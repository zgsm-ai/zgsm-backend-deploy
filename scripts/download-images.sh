#!/bin/bash

# 使用getopt解析参数
TEMP=$(getopt -o b:o: --long base-url:,output: -n "$0" -- "$@")
eval set -- "$TEMP"

# 默认值
base_url="https://zgsm.sangfor.com/images/"
output_dir="./images"

# 解析参数
while true ; do
    case "$1" in
        -b|--base-url)
            base_url="$2"
            shift 2
            ;;
        -o|--output)
            output_dir="$2"
            shift 2
            ;;
        --) shift ; break ;;
        *) echo "参数解析错误" >&2 ; exit 1 ;;
    esac
done

# 检查参数是否设置
if [ -z "$output_dir" ]; then
    echo "必须指定输出目录: -o|--output"
    exit 1
fi

# 确保base_url以/结尾
[[ "$base_url" != */ ]] && base_url="$base_url/"
list_url="https://zgsm.sangfor.com/images/image-files.list"
temp_list="$output_dir/image-files.list"

# 检测下载工具
download_cmd=""
if command -v wget >/dev/null 2>&1; then
    download_cmd="wget -q"
elif command -v curl >/dev/null 2>&1; then
    download_cmd="curl -s -O"
else
    echo "错误：未找到wget或curl命令" >&2
    exit 1
fi

# 创建输出目录
mkdir -p "$output_dir"

# 下载文件列表
echo "正在下载文件列表..."
if [ "$download_cmd" = "wget -q" ]; then
    if ! wget -q "$list_url" -O "$temp_list"; then
        echo "无法下载文件列表"
        exit 1
    fi
else # curl
    if ! curl -s -o "$temp_list" "$list_url"; then
        echo "无法下载文件列表"
        exit 1
    fi
fi

# 处理每个文件
while read -r filename; do
    # 跳过空行
    if [ -z "$filename" ]; then
        continue
    fi
    
    # 构建完整URL
    file_url="${base_url}${filename}"
    output_path="${output_dir}/${filename}"
    
    echo "正在下载: $filename"
    if [ "$download_cmd" = "wget -q" ]; then
        if ! wget -q "$file_url" -O "$output_path"; then
            echo "下载失败: $filename"
        else 
            echo "下载成功: $filename"
        fi
    else # curl
        if ! curl -s -o "$output_path" "$file_url"; then
            echo "下载失败: $filename"
        else 
            echo "下载成功: $filename"
        fi
    fi
done < "$temp_list"

echo "所有文件下载完成"