#!/bin/bash

# 脚本用途：读取镜像列表文件，停止并删除基于这些镜像启动的所有容器
# 作者：自动生成
# 版本：1.0

# 使用getopt解析参数
TEMP=$(getopt -o f:h --long file:,help -n "$0" -- "$@")
if [ $? != 0 ]; then
    echo "参数解析错误" >&2
    exit 1
fi
eval set -- "$TEMP"

# 默认值
images_file="./images.list"

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

选项:
  -f, --file FILE    指定镜像列表文件 (默认: ./images.list)
  -h, --help         显示此帮助信息

描述:
  此脚本读取指定的镜像列表文件，查找本机所有基于这些镜像启动的容器，
  然后停止并删除这些容器。

示例:
  $0                           # 使用默认的 ./images.list 文件
  $0 -f /path/to/images.list   # 使用指定的镜像列表文件
  $0 --file custom.list        # 使用自定义镜像列表文件

注意:
  - 镜像列表文件每行一个镜像名称
  - 此操作不可逆，请谨慎使用
  - 需要 Docker 运行权限
EOF
}

# 解析参数
while true ; do
    case "$1" in
        -f|--file)
            images_file="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --) shift ; break ;;
        *) echo "参数解析错误" >&2 ; exit 1 ;;
    esac
done

# 检查Docker是否可用
if ! command -v docker >/dev/null 2>&1; then
    echo "错误：未找到docker命令，请确保Docker已安装并可用" >&2
    exit 1
fi

# 检查Docker服务是否运行
if ! docker info >/dev/null 2>&1; then
    echo "错误：Docker服务未运行或无权限访问" >&2
    exit 1
fi

# 检查镜像列表文件是否存在
if [ ! -f "$images_file" ]; then
    echo "错误：镜像列表文件 '$images_file' 不存在" >&2
    exit 1
fi

# 检查文件是否为空
if [ ! -s "$images_file" ]; then
    echo "警告：镜像列表文件 '$images_file' 为空" >&2
    exit 0
fi

echo "正在读取镜像列表文件: $images_file"

# 读取镜像列表，过滤空行和注释行
images=()
while IFS= read -r line; do
    # 去除行首尾空白字符
    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    # 跳过空行和以#开头的注释行
    if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
        images+=("$line")
    fi
done < "$images_file"

if [ ${#images[@]} -eq 0 ]; then
    echo "警告：镜像列表文件中没有有效的镜像名称"
    exit 0
fi

echo "找到 ${#images[@]} 个镜像："
printf "  %s\n" "${images[@]}"
echo

# 查找并处理容器
total_containers=0
stopped_containers=0
removed_containers=0

for image in "${images[@]}"; do
    echo "处理镜像: $image"
    
    # 查找基于此镜像的所有容器（包括已停止的）
    containers=$(docker ps -a --filter "ancestor=$image" --format "{{.ID}} {{.Names}} {{.Status}}" 2>/dev/null)
    
    if [ -z "$containers" ]; then
        echo "  未找到基于此镜像的容器"
        continue
    fi
    
    # 处理每个容器
    while IFS= read -r container_info; do
        if [ -z "$container_info" ]; then
            continue
        fi
        
        container_id=$(echo "$container_info" | awk '{print $1}')
        container_name=$(echo "$container_info" | awk '{print $2}')
        container_status=$(echo "$container_info" | awk '{print $3}')
        
        total_containers=$((total_containers + 1))
        
        echo "  找到容器: $container_name ($container_id) - 状态: $container_status"
        
        # 如果容器正在运行或重启中，先停止它
        if [[ "$container_status" == "Up" ]]; then
            echo "    正在停止容器..."
            if docker stop "$container_id" >/dev/null 2>&1; then
                echo "    容器已停止"
                stopped_containers=$((stopped_containers + 1))
            else
                echo "    警告：停止容器失败"
            fi
        elif [[ "$container_status" == "Restarting" ]]; then
            echo "    容器正在重启中，强制停止容器..."
            if docker kill "$container_id" >/dev/null 2>&1; then
                echo "    容器已强制停止"
                stopped_containers=$((stopped_containers + 1))
            else
                echo "    警告：强制停止容器失败"
            fi
        fi
        
        # 删除容器
        echo "    正在删除容器..."
        if docker rm "$container_id" >/dev/null 2>&1; then
            echo "    容器已删除"
            removed_containers=$((removed_containers + 1))
        else
            echo "    警告：删除容器失败"
        fi
        
    done <<< "$containers"
    
    echo
done

# 显示统计信息
echo "操作完成！"
echo "统计信息："
echo "  处理的镜像数量: ${#images[@]}"
echo "  找到的容器总数: $total_containers"
echo "  停止的容器数量: $stopped_containers"
echo "  删除的容器数量: $removed_containers"

if [ $total_containers -eq 0 ]; then
    echo "没有找到基于指定镜像的容器。"
elif [ $removed_containers -eq $total_containers ]; then
    echo "所有容器都已成功处理。"
else
    echo "警告：部分容器处理失败，请检查Docker权限或容器状态。"
    exit 1
fi