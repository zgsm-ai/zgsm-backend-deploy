#!/bin/bash

# 使用getopt解析参数
TEMP=$(getopt -o b:o: --long list-url:,output: -n "$0" -- "$@")
eval set -- "$TEMP"

# 默认值
list_url="https://zgsm.sangfor.com/shenma-images/images.list"
output_file="./images.list"

# 解析参数
while true ; do
    case "$1" in
        -b|--list-url)
            list_url="$2"
            shift 2
            ;;
        -o|--output)
            output_file="$2"
            shift 2
            ;;
        --) shift ; break ;;
        *) echo "参数解析错误" >&2 ; exit 1 ;;
    esac
done

# 检测下载工具
download_cmd=""
if command -v curl >/dev/null 2>&1; then
    download_cmd="curl"
elif command -v wget >/dev/null 2>&1; then
    download_cmd="wget"
else
    echo "错误：未找到wget或curl命令" >&2
    exit 1
fi

# 下载文件列表
echo "正在下载文件列表..."
if [ "$download_cmd" = "wget" ]; then
    if ! wget -q "$list_url" -O "$output_file"; then
        echo "无法下载文件列表"
        exit 1
    fi
else # curl
    if ! curl -s -o "$output_file" "$list_url"; then
        echo "无法下载文件列表"
        exit 1
    fi
fi

echo "镜像列表下载成功，已保存到$output_file"
