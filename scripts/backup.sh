#!/bin/bash

# PostgreSQL 数据备份脚本
# 作者: 系统管理员
# 创建时间: $(date)
# 用途: 备份PostgreSQL数据库到指定目录

set -e  # 遇到错误时退出

# 配置变量
POSTGRES_DATA_DIR="postgres/data"
BACKUP_DIR="backups/postgres"
BACKUP_DATE=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/backup_${BACKUP_DATE}.log"

# 数据库连接配置
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_PASSWORD="${POSTGRES_PASSWORD}"
DB_NAMES="${POSTGRES_DATABASES:-chatgpt,auth,quota_manager,codereview,casdoor,codebase_indexer}"

# 备份选项
BACKUP_TYPE="all"  # data, logical, config, all
DRY_RUN="false"
FORCE_BACKUP="false"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "$LOG_FILE"
}

# 显示帮助信息
show_help() {
    cat << EOF
PostgreSQL 数据备份脚本

用法: $0 [选项]

选项:
  -h, --help              显示此帮助信息
  -t, --type TYPE         备份类型: data|logical|config|all (默认: all)
  -d, --database NAME     指定要备份的数据库名称 (多个用逗号分隔)
  --list-databases        列出可用的数据库
  --dry-run              预览模式，不执行实际备份
  --force                 强制备份，跳过确认
  --retention DAYS        备份保留天数 (默认: 7天)

备份类型说明:
  data      - 备份PostgreSQL数据文件 (物理备份)
  logical   - 备份数据库逻辑数据 (SQL转储)
  config    - 备份配置文件和脚本
  all       - 执行完整备份 (包含以上所有)

环境变量:
  POSTGRES_HOST           PostgreSQL主机地址 (默认: localhost)
  POSTGRES_PORT           PostgreSQL端口 (默认: 5432)
  POSTGRES_USER           PostgreSQL用户名 (默认: postgres)
  POSTGRES_PASSWORD       PostgreSQL密码
  POSTGRES_DATABASES      要备份的数据库 (默认: all)
  BACKUP_RETENTION_DAYS   备份保留天数 (默认: 7)

示例:
  $0                                    # 执行完整备份
  $0 --help                            # 显示帮助信息
  $0 --list-databases                  # 列出数据库
  $0 -t data                          # 仅备份数据文件
  $0 -t logical -d mydb,testdb        # 备份指定数据库
  $0 --dry-run                        # 预览备份操作
  $0 --force --retention 30          # 强制备份，保留30天

EOF
}

# 创建必要的目录
create_directories() {
    log "创建备份目录..."
    mkdir -p "$BACKUP_DIR"
    mkdir -p "logs"
    mkdir -p "$POSTGRES_DATA_DIR"
}

# 列出可用的数据库
list_databases() {
    log "获取可用数据库列表..."
    
    if ! command -v psql >/dev/null 2>&1; then
        error "psql 命令不可用"
        return 1
    fi
    
    export PGPASSWORD="$DB_PASSWORD"
    
    local databases
    databases=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -t -c \
        "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;" \
        2>/dev/null | grep -v "^$" | tr -d ' ')
    
    unset PGPASSWORD
    
    if [ -z "$databases" ]; then
        warning "未找到数据库"
        return 1
    fi
    
    info "=== 可用数据库列表 ==="
    echo "$databases" | while read -r db; do
        # 获取数据库大小
        export PGPASSWORD="$DB_PASSWORD"
        local size=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$db" -t -c \
            "SELECT pg_size_pretty(pg_database_size('$db'));" 2>/dev/null | tr -d ' ')
        unset PGPASSWORD
        
        if [ -n "$size" ]; then
            echo "  $db ($size)"
        else
            echo "  $db"
        fi
    done
    info "====================="
}

# 检查PostgreSQL服务状态
check_postgres_status() {
    log "检查PostgreSQL服务状态..."
    
    if command -v docker >/dev/null 2>&1; then
        if docker ps | grep -q postgres; then
            log "PostgreSQL Docker容器正在运行"
            return 0
        fi
    fi
    
    if command -v systemctl >/dev/null 2>&1; then
        if systemctl is-active --quiet postgresql; then
            log "PostgreSQL服务正在运行"
            return 0
        fi
    fi
    
    if command -v pg_isready >/dev/null 2>&1; then
        if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" >/dev/null 2>&1; then
            log "PostgreSQL数据库可连接"
            return 0
        fi
    fi
    
    warning "PostgreSQL服务状态未知，继续执行备份..."
    return 0
}

# 备份数据库文件
backup_data_files() {
    log "开始备份PostgreSQL数据文件..."
    
    if [ -d "$POSTGRES_DATA_DIR" ]; then
        DATA_BACKUP_FILE="$BACKUP_DIR/postgres_data_${BACKUP_DATE}.tar.gz"
        
        log "压缩数据目录: $POSTGRES_DATA_DIR -> $DATA_BACKUP_FILE"
        tar -czf "$DATA_BACKUP_FILE" -C "postgres" data/ 2>/dev/null || {
            error "数据文件备份失败"
            return 1
        }
        
        log "数据文件备份完成: $DATA_BACKUP_FILE"
        log "备份文件大小: $(du -h "$DATA_BACKUP_FILE" | cut -f1)"
    else
        warning "数据目录不存在: $POSTGRES_DATA_DIR"
    fi
}

# 备份单个数据库
backup_single_database() {
    local db_name="$1"
    local dump_file="$BACKUP_DIR/${db_name}_${BACKUP_DATE}.sql"
    
    log "备份数据库: $db_name"
    
    export PGPASSWORD="$DB_PASSWORD"
    
    if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$db_name" \
        --clean --create --if-exists --verbose > "$dump_file" 2>>"$LOG_FILE"; then
        
        # 压缩SQL文件
        gzip "$dump_file"
        log "数据库备份完成: ${dump_file}.gz"
        log "备份文件大小: $(du -h "${dump_file}.gz" | cut -f1)"
    else
        error "数据库 $db_name 备份失败"
        return 1
    fi
    
    unset PGPASSWORD
}

# 备份所有数据库
backup_all_databases() {
    log "获取数据库列表..."
    
    export PGPASSWORD="$DB_PASSWORD"
    
    local databases
    databases=$(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -t -c \
        "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres';" \
        2>/dev/null | grep -v "^$" | tr -d ' ')
    
    if [ -z "$databases" ]; then
        warning "未找到用户数据库，将备份默认数据库"
        databases="postgres"
    fi
    
    unset PGPASSWORD
    
    log "找到数据库: $(echo $databases | tr '\n' ' ')"
    
    for db in $databases; do
        backup_single_database "$db"
    done
}

# 备份数据库逻辑数据
backup_database_logical() {
    log "开始备份PostgreSQL数据库..."
    
    # 检查必要的命令
    if ! command -v pg_dump >/dev/null 2>&1; then
        warning "pg_dump 命令不可用，跳过逻辑备份"
        return 0
    fi
    
    if [ "$DB_NAMES" = "all" ]; then
        backup_all_databases
    else
        IFS=',' read -ra DB_ARRAY <<< "$DB_NAMES"
        for db in "${DB_ARRAY[@]}"; do
            backup_single_database "$(echo "$db" | tr -d ' ')"
        done
    fi
}

# 备份配置文件
backup_configs() {
    log "备份PostgreSQL配置文件..."
    
    CONFIG_BACKUP_DIR="$BACKUP_DIR/configs_${BACKUP_DATE}"
    mkdir -p "$CONFIG_BACKUP_DIR"
    
    # 备份initdb.d目录
    if [ -d "postgres/initdb.d" ]; then
        cp -r postgres/initdb.d "$CONFIG_BACKUP_DIR/"
        log "已备份初始化脚本"
    fi
    
    # 备份scripts目录
    if [ -d "postgres/scripts" ]; then
        cp -r postgres/scripts "$CONFIG_BACKUP_DIR/"
        log "已备份SQL脚本"
    fi
    
    # 压缩配置文件
    tar -czf "$BACKUP_DIR/postgres_configs_${BACKUP_DATE}.tar.gz" \
        -C "$BACKUP_DIR" "configs_${BACKUP_DATE}" 2>/dev/null
    
    rm -rf "$CONFIG_BACKUP_DIR"
    log "配置文件备份完成"
}

# 用户确认
confirm_backup() {
    if [ "$FORCE_BACKUP" = "true" ]; then
        return 0
    fi
    
    info "即将执行备份操作:"
    info "  备份类型: $BACKUP_TYPE"
    info "  备份目录: $BACKUP_DIR"
    
    if [ "$BACKUP_TYPE" = "logical" ] || [ "$BACKUP_TYPE" = "all" ]; then
        info "  数据库: $DB_NAMES"
    fi
    
    read -p "确认执行备份？[y/N]: " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "用户取消备份操作"
        return 1
    fi
}

# 预览备份操作
preview_backup() {
    log "=== 备份预览模式 ==="
    log "备份类型: $BACKUP_TYPE"
    log "备份目录: $BACKUP_DIR"
    log "备份时间: $BACKUP_DATE"
    
    case "$BACKUP_TYPE" in
        "data")
            log "将备份数据目录: $POSTGRES_DATA_DIR"
            ;;
        "logical")
            log "将备份数据库: $DB_NAMES"
            ;;
        "config")
            log "将备份配置文件和脚本"
            ;;
        "all")
            log "将执行完整备份:"
            log "  - 数据文件备份"
            log "  - 逻辑数据备份 ($DB_NAMES)"
            log "  - 配置文件备份"
            ;;
    esac
    
    log "预计备份文件:"
    case "$BACKUP_TYPE" in
        "data"|"all")
            log "  - postgres_data_${BACKUP_DATE}.tar.gz"
            ;;
    esac
    
    case "$BACKUP_TYPE" in
        "logical"|"all")
            if [ "$DB_NAMES" = "all" ]; then
                log "  - <database_name>_${BACKUP_DATE}.sql.gz (每个数据库)"
            else
                IFS=',' read -ra DB_ARRAY <<< "$DB_NAMES"
                for db in "${DB_ARRAY[@]}"; do
                    db=$(echo "$db" | tr -d ' ')
                    log "  - ${db}_${BACKUP_DATE}.sql.gz"
                done
            fi
            ;;
    esac
    
    case "$BACKUP_TYPE" in
        "config"|"all")
            log "  - postgres_configs_${BACKUP_DATE}.tar.gz"
            ;;
    esac
    
    log "=================="
}

# 清理旧备份
cleanup_old_backups() {
    local keep_days="${BACKUP_RETENTION_DAYS:-7}"
    
    log "清理 $keep_days 天前的旧备份文件..."
    
    find "$BACKUP_DIR" -name "*.tar.gz" -type f -mtime +$keep_days -delete 2>/dev/null || true
    find "$BACKUP_DIR" -name "*.sql.gz" -type f -mtime +$keep_days -delete 2>/dev/null || true
    find "logs" -name "backup_*.log" -type f -mtime +$keep_days -delete 2>/dev/null || true
    
    log "旧备份清理完成"
}

# 生成备份报告
generate_report() {
    local backup_files
    backup_files=$(find "$BACKUP_DIR" -name "*${BACKUP_DATE}*" -type f)
    
    log "=== 备份完成报告 ==="
    log "备份时间: $(date)"
    log "备份目录: $BACKUP_DIR"
    log "备份文件:"
    
    if [ -n "$backup_files" ]; then
        echo "$backup_files" | while read -r file; do
            log "  - $(basename "$file") ($(du -h "$file" | cut -f1))"
        done
        
        local total_size
        total_size=$(du -sh "$BACKUP_DIR" | cut -f1)
        log "总备份大小: $total_size"
    else
        warning "未找到备份文件"
    fi
    
    log "备份日志: $LOG_FILE"
    log "===================="
}

# 执行备份操作
perform_backup() {
    case "$BACKUP_TYPE" in
        "data")
            backup_data_files
            ;;
        "logical")
            backup_database_logical
            ;;
        "config")
            backup_configs
            ;;
        "all")
            backup_data_files
            backup_database_logical
            backup_configs
            ;;
        *)
            error "未知的备份类型: $BACKUP_TYPE"
            return 1
            ;;
    esac
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--type)
                BACKUP_TYPE="$2"
                shift 2
                ;;
            -d|--database)
                DB_NAMES="$2"
                shift 2
                ;;
            --list-databases)
                create_directories
                list_databases
                exit 0
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --force)
                FORCE_BACKUP="true"
                shift
                ;;
            --retention)
                BACKUP_RETENTION_DAYS="$2"
                shift 2
                ;;
            *)
                error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 验证备份类型
    case "$BACKUP_TYPE" in
        "data"|"logical"|"config"|"all")
            ;;
        *)
            error "无效的备份类型: $BACKUP_TYPE"
            error "支持的类型: data, logical, config, all"
            exit 1
            ;;
    esac
}

# 主函数
main() {
    parse_args "$@"
    
    log "开始PostgreSQL数据备份..."
    log "备份标识: $BACKUP_DATE"
    log "备份类型: $BACKUP_TYPE"
    
    create_directories
    
    if [ "$DRY_RUN" = "true" ]; then
        preview_backup
        return 0
    fi
    
    check_postgres_status
    
    confirm_backup
    
    perform_backup
    
    cleanup_old_backups
    
    generate_report
    
    log "PostgreSQL备份任务完成！"
}

# 脚本入口点
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi