#!/bin/bash

# PostgreSQL 数据恢复脚本
# 作者: 系统管理员
# 创建时间: $(date)
# 用途: 从备份文件恢复PostgreSQL数据库

set -e  # 遇到错误时退出

# 配置变量
POSTGRES_DATA_DIR="postgres/data"
BACKUP_DIR="backups/postgres"
RESTORE_DATE=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/restore_${RESTORE_DATE}.log"

# 数据库连接配置
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_PASSWORD="${POSTGRES_PASSWORD}"

# 恢复选项
BACKUP_FILE=""
RESTORE_TYPE=""  # data, logical, config, all
TARGET_DATABASE=""

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
PostgreSQL 数据恢复脚本

用法: $0 [选项]

选项:
  -h, --help              显示此帮助信息
  -f, --file FILE         指定备份文件路径
  -t, --type TYPE         恢复类型: data|logical|config|all (默认: all)
  -d, --database NAME     目标数据库名称 (仅用于逻辑恢复)
  --list-backups         列出可用的备份文件
  --dry-run              预览模式，不执行实际恢复
  --force                 强制恢复，不进行确认

环境变量:
  POSTGRES_HOST           PostgreSQL主机地址 (默认: localhost)
  POSTGRES_PORT           PostgreSQL端口 (默认: 5432)
  POSTGRES_USER           PostgreSQL用户名 (默认: postgres)
  POSTGRES_PASSWORD       PostgreSQL密码

示例:
  $0 --list-backups                           # 列出可用备份
  $0 -f postgres_data_20240106_143000.tar.gz  # 恢复数据文件
  $0 -t logical -d mydb                       # 恢复指定数据库
  $0 -t all --force                          # 完整恢复

EOF
}

# 创建必要的目录
create_directories() {
    log "创建恢复工作目录..."
    mkdir -p "logs"
    mkdir -p "temp/restore_${RESTORE_DATE}"
}

# 列出可用的备份文件
list_backups() {
    log "扫描可用的备份文件..."
    
    if [ ! -d "$BACKUP_DIR" ]; then
        error "备份目录不存在: $BACKUP_DIR"
        return 1
    fi
    
    local backup_files
    backup_files=$(find "$BACKUP_DIR" -name "*.tar.gz" -o -name "*.sql.gz" | sort -r)
    
    if [ -z "$backup_files" ]; then
        warning "未找到备份文件"
        return 1
    fi
    
    info "=== 可用的备份文件 ==="
    echo "$backup_files" | while read -r file; do
        local size=$(du -h "$file" | cut -f1)
        local date=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null | cut -d'.' -f1)
        echo "  $(basename "$file") (${size}, ${date})"
    done
    info "========================"
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
    
    error "PostgreSQL服务未运行或无法连接"
    return 1
}

# 停止PostgreSQL服务
stop_postgres() {
    log "停止PostgreSQL服务..."
    
    if command -v docker >/dev/null 2>&1; then
        local postgres_container=$(docker ps --format "table {{.Names}}" | grep postgres | head -n1)
        if [ -n "$postgres_container" ]; then
            docker stop "$postgres_container" || true
            log "已停止PostgreSQL Docker容器: $postgres_container"
            return 0
        fi
    fi
    
    if command -v systemctl >/dev/null 2>&1; then
        systemctl stop postgresql || true
        log "已停止PostgreSQL系统服务"
        return 0
    fi
    
    warning "无法自动停止PostgreSQL服务，请手动停止"
}

# 启动PostgreSQL服务
start_postgres() {
    log "启动PostgreSQL服务..."
    
    if command -v docker >/dev/null 2>&1; then
        local postgres_container=$(docker ps -a --format "table {{.Names}}" | grep postgres | head -n1)
        if [ -n "$postgres_container" ]; then
            docker start "$postgres_container" || true
            sleep 5  # 等待服务启动
            log "已启动PostgreSQL Docker容器: $postgres_container"
            return 0
        fi
    fi
    
    if command -v systemctl >/dev/null 2>&1; then
        systemctl start postgresql || true
        sleep 5  # 等待服务启动
        log "已启动PostgreSQL系统服务"
        return 0
    fi
    
    warning "无法自动启动PostgreSQL服务，请手动启动"
}

# 恢复数据文件
restore_data_files() {
    local backup_file="$1"
    
    if [ ! -f "$backup_file" ]; then
        error "备份文件不存在: $backup_file"
        return 1
    fi
    
    log "开始恢复PostgreSQL数据文件..."
    log "备份文件: $backup_file"
    
    # 停止PostgreSQL服务
    stop_postgres
    
    # 备份当前数据目录
    if [ -d "$POSTGRES_DATA_DIR" ]; then
        local current_backup="temp/restore_${RESTORE_DATE}/current_data_backup.tar.gz"
        log "备份当前数据目录到: $current_backup"
        tar -czf "$current_backup" -C "postgres" data/ 2>/dev/null || true
    fi
    
    # 清空当前数据目录
    log "清空当前数据目录..."
    rm -rf "$POSTGRES_DATA_DIR"
    mkdir -p "postgres"
    
    # 解压备份文件
    log "解压备份文件..."
    if tar -xzf "$backup_file" -C "postgres" 2>/dev/null; then
        log "数据文件恢复完成"
    else
        error "数据文件解压失败"
        
        # 尝试恢复原有数据
        if [ -f "temp/restore_${RESTORE_DATE}/current_data_backup.tar.gz" ]; then
            log "正在恢复原有数据..."
            tar -xzf "temp/restore_${RESTORE_DATE}/current_data_backup.tar.gz" -C "postgres" 2>/dev/null || true
        fi
        
        start_postgres
        return 1
    fi
    
    # 启动PostgreSQL服务
    start_postgres
    
    # 等待服务完全启动
    log "等待PostgreSQL服务启动..."
    local retry_count=0
    while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" >/dev/null 2>&1; do
        sleep 2
        retry_count=$((retry_count + 1))
        if [ $retry_count -gt 30 ]; then
            error "PostgreSQL服务启动超时"
            return 1
        fi
    done
    
    log "数据文件恢复成功"
}

# 恢复单个数据库
restore_single_database() {
    local sql_file="$1"
    local target_db="$2"
    
    if [ ! -f "$sql_file" ]; then
        error "SQL备份文件不存在: $sql_file"
        return 1
    fi
    
    log "恢复数据库: $target_db"
    log "SQL文件: $sql_file"
    
    export PGPASSWORD="$DB_PASSWORD"
    
    # 解压SQL文件（如果是压缩的）
    local temp_sql_file="$sql_file"
    if [[ "$sql_file" == *.gz ]]; then
        temp_sql_file="temp/restore_${RESTORE_DATE}/$(basename "$sql_file" .gz)"
        log "解压SQL文件..."
        gunzip -c "$sql_file" > "$temp_sql_file"
    fi
    
    # 恢复数据库
    if [ -n "$target_db" ]; then
        # 恢复到指定数据库
        if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$target_db" \
            -f "$temp_sql_file" >>"$LOG_FILE" 2>&1; then
            log "数据库 $target_db 恢复成功"
        else
            error "数据库 $target_db 恢复失败"
            unset PGPASSWORD
            return 1
        fi
    else
        # 使用SQL文件中的建库语句
        if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
            -f "$temp_sql_file" >>"$LOG_FILE" 2>&1; then
            log "数据库恢复成功"
        else
            error "数据库恢复失败"
            unset PGPASSWORD
            return 1
        fi
    fi
    
    # 清理临时文件
    if [[ "$sql_file" == *.gz ]] && [ -f "$temp_sql_file" ]; then
        rm -f "$temp_sql_file"
    fi
    
    unset PGPASSWORD
}

# 恢复配置文件
restore_configs() {
    local config_file="$1"
    
    if [ ! -f "$config_file" ]; then
        error "配置备份文件不存在: $config_file"
        return 1
    fi
    
    log "恢复PostgreSQL配置文件..."
    log "配置文件: $config_file"
    
    # 备份当前配置
    local current_config_backup="temp/restore_${RESTORE_DATE}/current_configs.tar.gz"
    if [ -d "postgres/initdb.d" ] || [ -d "postgres/scripts" ]; then
        log "备份当前配置..."
        tar -czf "$current_config_backup" postgres/initdb.d postgres/scripts 2>/dev/null || true
    fi
    
    # 解压配置文件
    local temp_dir="temp/restore_${RESTORE_DATE}/configs"
    mkdir -p "$temp_dir"
    
    if tar -xzf "$config_file" -C "$temp_dir" 2>/dev/null; then
        # 查找解压后的配置目录
        local config_dir=$(find "$temp_dir" -name "configs_*" -type d | head -n1)
        
        if [ -n "$config_dir" ]; then
            # 恢复initdb.d目录
            if [ -d "$config_dir/initdb.d" ]; then
                rm -rf postgres/initdb.d
                cp -r "$config_dir/initdb.d" postgres/
                log "已恢复初始化脚本"
            fi
            
            # 恢复scripts目录
            if [ -d "$config_dir/scripts" ]; then
                rm -rf postgres/scripts
                cp -r "$config_dir/scripts" postgres/
                log "已恢复SQL脚本"
            fi
            
            log "配置文件恢复完成"
        else
            error "配置文件格式不正确"
            return 1
        fi
    else
        error "配置文件解压失败"
        return 1
    fi
    
    # 清理临时目录
    rm -rf "$temp_dir"
}

# 自动选择备份文件
auto_select_backup() {
    local backup_type="$1"
    local pattern=""
    
    case "$backup_type" in
        "data")
            pattern="postgres_data_*.tar.gz"
            ;;
        "logical")
            pattern="*.sql.gz"
            ;;
        "config")
            pattern="postgres_configs_*.tar.gz"
            ;;
        *)
            error "未知的备份类型: $backup_type"
            return 1
            ;;
    esac
    
    local latest_file=$(find "$BACKUP_DIR" -name "$pattern" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | head -n1 | cut -d' ' -f2-)
    
    if [ -n "$latest_file" ]; then
        echo "$latest_file"
    else
        return 1
    fi
}

# 用户确认
confirm_restore() {
    if [ "$FORCE_RESTORE" = "true" ]; then
        return 0
    fi
    
    warning "此操作将覆盖现有数据，请确认是否继续？"
    read -p "输入 'yes' 继续，其他任意键取消: " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log "用户取消恢复操作"
        return 1
    fi
}

# 生成恢复报告
generate_report() {
    log "=== 恢复完成报告 ==="
    log "恢复时间: $(date)"
    log "恢复类型: $RESTORE_TYPE"
    
    if [ -n "$BACKUP_FILE" ]; then
        log "使用备份: $(basename "$BACKUP_FILE")"
    fi
    
    if [ -n "$TARGET_DATABASE" ]; then
        log "目标数据库: $TARGET_DATABASE"
    fi
    
    log "恢复日志: $LOG_FILE"
    log "===================="
}

# 主恢复函数
perform_restore() {
    case "$RESTORE_TYPE" in
        "data")
            if [ -z "$BACKUP_FILE" ]; then
                BACKUP_FILE=$(auto_select_backup "data")
                if [ $? -ne 0 ]; then
                    error "未找到数据备份文件"
                    return 1
                fi
                log "自动选择数据备份: $(basename "$BACKUP_FILE")"
            fi
            restore_data_files "$BACKUP_FILE"
            ;;
        "logical")
            if [ -z "$BACKUP_FILE" ]; then
                BACKUP_FILE=$(auto_select_backup "logical")
                if [ $? -ne 0 ]; then
                    error "未找到逻辑备份文件"
                    return 1
                fi
                log "自动选择逻辑备份: $(basename "$BACKUP_FILE")"
            fi
            restore_single_database "$BACKUP_FILE" "$TARGET_DATABASE"
            ;;
        "config")
            if [ -z "$BACKUP_FILE" ]; then
                BACKUP_FILE=$(auto_select_backup "config")
                if [ $? -ne 0 ]; then
                    error "未找到配置备份文件"
                    return 1
                fi
                log "自动选择配置备份: $(basename "$BACKUP_FILE")"
            fi
            restore_configs "$BACKUP_FILE"
            ;;
        "all")
            log "执行完整恢复..."
            
            # 恢复配置文件
            local config_file=$(auto_select_backup "config")
            if [ -n "$config_file" ]; then
                restore_configs "$config_file"
            fi
            
            # 恢复数据文件
            local data_file=$(auto_select_backup "data")
            if [ -n "$data_file" ]; then
                restore_data_files "$data_file"
            fi
            
            # 恢复逻辑数据
            local sql_files=$(find "$BACKUP_DIR" -name "*.sql.gz" -type f | head -5)
            if [ -n "$sql_files" ]; then
                echo "$sql_files" | while read -r sql_file; do
                    restore_single_database "$sql_file" ""
                done
            fi
            ;;
        *)
            error "未知的恢复类型: $RESTORE_TYPE"
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
            -f|--file)
                BACKUP_FILE="$2"
                shift 2
                ;;
            -t|--type)
                RESTORE_TYPE="$2"
                shift 2
                ;;
            -d|--database)
                TARGET_DATABASE="$2"
                shift 2
                ;;
            --list-backups)
                list_backups
                exit 0
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --force)
                FORCE_RESTORE="true"
                shift
                ;;
            *)
                error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 设置默认值
    if [ -z "$RESTORE_TYPE" ]; then
        RESTORE_TYPE="all"
    fi
}

# 主函数
main() {
    parse_args "$@"
    
    log "开始PostgreSQL数据恢复..."
    log "恢复标识: $RESTORE_DATE"
    log "恢复类型: $RESTORE_TYPE"
    
    create_directories
    
    if [ "$DRY_RUN" = "true" ]; then
        log "预览模式 - 不执行实际恢复"
        list_backups
        return 0
    fi
    
    check_postgres_status
    
    confirm_restore
    
    perform_restore
    
    generate_report
    
    log "PostgreSQL恢复任务完成！"
}

# 脚本入口点
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi