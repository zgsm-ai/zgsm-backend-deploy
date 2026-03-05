#!/bin/bash

# 脚本用途：清理项目目录下的存储目录
# 作者：自动生成
# 版本：1.0

# 使用getopt解析参数
TEMP=$(getopt -o hfy --long help,force,yes -n "$0" -- "$@")
if [ $? != 0 ]; then
    echo "参数解析错误" >&2
    exit 1
fi
eval set -- "$TEMP"

# 默认值
FORCE_DELETE=false
AUTO_CONFIRM=false

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

选项:
  -h, --help         显示此帮助信息
  -f, --force        强制删除，不进行确认
  -y, --yes          自动回答"是"到所有提示

描述:
  此脚本用于删除项目目录下的存储目录，包括：
  - weviate 目录
  - redis 目录
  - postgres/data 目录
  - etcd/data 目录
  - es 目录

示例:
  $0                          # 交互式删除
  $0 -f                       # 强制删除，不进行确认
  $0 -y                       # 自动回答"是"到所有提示
  $0 -f -y                    # 强制删除并自动确认

注意:
  - 此操作将永久删除数据，不可恢复
  - 请确保在执行前已备份重要数据
  - 建议在执行此脚本前先停止相关服务
EOF
}

# 解析参数
while true ; do
    case "$1" in
        -f|--force)
            FORCE_DELETE=true
            shift
            ;;
        -y|--yes)
            AUTO_CONFIRM=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --) shift ; break ;;
        *) echo "参数解析错误" >&2 ; exit 1 ;;
    esac
done

# 定义要清理的目录列表
DIRECTORIES_TO_CLEAN=(
    "weaviate"
    "redis"
    "postgres/data"
    "etcd/data"
    "es"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[信息]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

log_error() {
    echo -e "${RED}[错误]${NC} $1"
}

log_header() {
    echo -e "${BLUE}$1${NC}"
}

# 确认函数
confirm_action() {
    if [ "$AUTO_CONFIRM" = true ] || [ "$FORCE_DELETE" = true ]; then
        return 0
    fi
    
    while true; do
        read -p "确定要删除这些目录吗？(y/n): " -r
        case $REPLY in
            [Yy]) return 0 ;;
            [Nn]) 
                log_info "操作已取消"
                exit 0
                ;;
            *) echo "请输入 y 或 n" ;;
        esac
    done
}

# 删除目录函数
remove_directory() {
    local dir_path="$1"
    
    if [ ! -e "$dir_path" ]; then
        log_info "目录不存在，跳过: $dir_path"
        return 0
    fi
    
    log_info "正在删除: $dir_path"
    
    if [ "$FORCE_DELETE" = true ]; then
        rm -rf "$dir_path" 2>/dev/null
    else
        # 尝试正常删除
        rm -rf "$dir_path" 2>/dev/null
    fi
    
    if [ $? -eq 0 ]; then
        log_info "成功删除: $dir_path"
        return 0
    else
        log_error "删除失败: $dir_path"
        return 1
    fi
}

# 显示将要删除的目录
show_directories_to_remove() {
    log_header "将要删除以下目录："
    
    local count=0
    for dir in "${DIRECTORIES_TO_CLEAN[@]}"; do
        if [ -e "$dir" ]; then
            local size=""
            if [ -d "$dir" ]; then
                size=" ($(du -sh "$dir" 2>/dev/null | cut -f1 || echo "未知大小")"
            fi
            echo "  - $dir$size"
            count=$((count + 1))
        fi
    done
    
    if [ $count -eq 0 ]; then
        log_info "没有找到需要删除的目录"
        exit 0
    fi
    
    echo
}

# 主函数
main() {
    log_header "=== 存储清理脚本 ==="
    
    # 显示将要删除的目录
    show_directories_to_remove
    
    # 确认操作
    if [ "$FORCE_DELETE" != true ]; then
        confirm_action
    else
        log_warning "强制模式，跳过确认步骤"
    fi
    
    echo
    log_header "开始清理..."
    
    # 统计信息
    local total=0
    local success=0
    local failed=0
    
    # 删除目录
    for dir in "${DIRECTORIES_TO_CLEAN[@]}"; do
        if [ -e "$dir" ]; then
            total=$((total + 1))
            if remove_directory "$dir"; then
                success=$((success + 1))
            else
                failed=$((failed + 1))
            fi
        fi
    done
    
    echo
    log_header "=== 清理完成 ==="
    log_info "处理总数: $total"
    log_info "成功删除: $success"
    
    if [ $failed -gt 0 ]; then
        log_error "删除失败: $failed"
        exit 1
    else
        log_info "所有目录清理成功完成"
    fi
}

# 执行主函数
main