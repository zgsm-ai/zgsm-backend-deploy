#!/bin/bash

# 本脚本运行的前提条件：
#   1. linux机器
#   2. 安装了docker
#

# 从.env文件读取配置
if [ -f "$(dirname "$0")/.env" ]; then
    # shellcheck disable=SC1090
    source "$(dirname "$0")/.env"
else
    echo "Error: .env file not found in $(dirname "$0")"
    exit 1
fi

LOAD_DIR="./images"

function usage() {
    echo "Usage: push-images.sh [options]"
    echo "Push docker images to Harbor registry"
    echo ""
    echo "Options:"
    echo "  -l <LOAD_DIR>    Load all images from directory (default: ./images)"
    echo "  -f <IMAGE_FILE>  Push specific image file"
    echo "  -s <HOST>        Harbor host (default: harbor.sangfor.com)"
    echo "  -r <REPO>        Harbor repository (default: zgsm)"
    echo "  -u <USER>        Harbor username (default: admin)"
    echo "  -p <PASS>        Harbor password (default: )"
    echo "  -h               Show this help message"
    echo ""
    echo "Examples:"
    echo "  # Push all images from directory"
    echo "  push-images.sh -l ./images"
    echo ""
    echo "  # Push single image file"
    echo "  push-images.sh -f ./images/nginx.tar"
    echo ""
    echo "  # Customize Harbor parameters"
    echo "  push-images.sh -l ./images -s myharbor.com -u myuser"
}

while getopts "l:f:s:r:u:p:h" opt
do
    case $opt in
    l)
        LOAD_DIR=$OPTARG
        ;;
    f)
        SPECIFIC_FILE=$OPTARG
        ;;
    s)
        DH_HOST=$OPTARG
        ;;
    r)
        DH_REPO=$OPTARG
        ;;
    u)
        DH_USER=$OPTARG
        ;;
    p)
        DH_PASS=$OPTARG
        ;;
    ?)
        usage
        exit 1;;
    esac
done

echo LOAD_DIR = ${LOAD_DIR}

function push_images() {
    docker login "$DH_HOST" --username "$DH_USER" --password "$DH_PASS"

    if [ -n "$SPECIFIC_FILE" ]; then
        # 上传单个指定文件
        push_single_image "$SPECIFIC_FILE"
    else
        # 上传目录下所有文件
        for image in `ls "${LOAD_DIR}"/*.tar`; do
            if [ ! -f ${image} ]; then
                continue
            fi
            push_single_image "$image"
        done
    fi
}

function push_single_image() {
    local image=$1
    
    # 执行 docker load 命令并捕获输出
    output=$(docker load -i "$image" 2>&1)

    # 检查命令是否成功执行
    if echo "$output" | grep -q "Loaded image:"; then
        # 提取镜像名和TAG
        IMAGE=$(echo "$output" | grep "Loaded image:" | awk '{print $3}')
        IMAGE_NAME=$(basename "$IMAGE" | cut -d: -f1)  # 获取镜像名最后一段
        IMAGE_TAG=$(basename "$IMAGE" | cut -d: -f2)   # 获取tag

        echo "docker tag $IMAGE $DH_HOST/$DH_REPO/$IMAGE_NAME:$IMAGE_TAG ..."
        docker tag "$IMAGE" "$DH_HOST/$DH_REPO/$IMAGE_NAME:$IMAGE_TAG"

        echo "Push image to $DH_HOST/$DH_REPO/$IMAGE_NAME:$IMAGE_TAG ..."
        docker push "$DH_HOST/$DH_REPO/$IMAGE_NAME:$IMAGE_TAG"

        echo "Push image to $DH_HOST/$DH_REPO/$IMAGE_NAME:latest"
        docker tag "$IMAGE" "$DH_HOST/$DH_REPO/$IMAGE_NAME:latest"
        docker push "$DH_HOST/$DH_REPO/$IMAGE_NAME:latest"
    else
        # 输出错误信息
        echo "Error loading image: $output"
        exit 1
    fi
}

push_images
