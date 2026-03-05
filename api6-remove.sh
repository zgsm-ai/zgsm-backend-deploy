#!/bin/sh

. ./configure.sh

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  --route ID     删除指定ID的路由"
    echo "  --upstream ID  删除指定ID的upstream"
    echo "  --help         显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 --route tunnel-manager     # 删除ID为tunnel-manager的路由"
    echo "  $0 --upstream tunnel-manager  # 删除ID为tunnel-manager的upstream"
    echo "  $0 --route route1 --upstream upstream1  # 同时删除路由和upstream"
}

# 初始化变量
ROUTE_ID=""
UPSTREAM_ID=""

# 使用getopt解析命令行参数
TEMP=$(getopt -o '' --long route:,upstream:,help -n "$0" -- "$@")

if [ $? != 0 ]; then
    echo "参数解析错误" >&2
    show_help
    exit 1
fi

eval set -- "$TEMP"

# 提取选项和参数
while true; do
    case "$1" in
        --route)
            ROUTE_ID="$2"
            shift 2
            ;;
        --upstream)
            UPSTREAM_ID="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "内部错误!" >&2
            exit 1
            ;;
    esac
done

# 检查是否至少指定了一个参数
if [ -z "$ROUTE_ID" ] && [ -z "$UPSTREAM_ID" ]; then
    echo "错误: 必须指定 --route 或 --upstream 参数"
    show_help
    exit 1
fi

# 删除路由
if [ -n "$ROUTE_ID" ]; then
    echo "正在删除路由: $ROUTE_ID"
    curl -i http://$APISIX_ADDR/apisix/admin/routes/$ROUTE_ID -H "$AUTH" -H "$TYPE" -X DELETE
    echo ""
fi

# 删除upstream
if [ -n "$UPSTREAM_ID" ]; then
    echo "正在删除upstream: $UPSTREAM_ID"
    curl -i http://$APISIX_ADDR/apisix/admin/upstreams/$UPSTREAM_ID -H "$AUTH" -H "$TYPE" -X DELETE
    echo ""
fi

echo "操作完成"