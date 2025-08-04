#!/bin/bash

# 本脚本运行的前提条件：
#   1. linux机器
#   2. 安装了docker
#
# 功能：为镜像列表中的每个镜像添加latest标签

IMAGE_LIST_FILE=""
IMAGE_LIST_STR=""

function usage() {
    echo "usage: tag-latest.sh [options]"
    echo "  为镜像添加latest标签"
    echo "options:"
    echo "  [-i <IMAGE_LIST_STR>] - 镜像列表字符串"
    echo "  [-f <IMAGE_LIST_FILE>] - 镜像列表文件"
    echo "examples:"
    echo "  tag-latest.sh -f images.list"
}

while getopts ":i:f:" opt
do
    case $opt in
    i)
        IMAGE_LIST_STR=$OPTARG
        ;;
    f)
        IMAGE_LIST_FILE=$OPTARG
        ;;
    ?)
        usage
        exit 1;;
    esac
done

IMAGES=""
if [ "${IMAGE_LIST_STR}" != "" ]; then
    IMAGES="${IMAGE_LIST_STR}"
fi

if [ "${IMAGE_LIST_FILE}" != "" ]; then
    IMAGES=`cat ${IMAGE_LIST_FILE}`
fi

function tag_latest() {
    for image in `echo ${IMAGES}`; do
        # 提取镜像名(去掉tag部分)
        image_name=${image%:*}
        echo "docker tag ${image} ${image_name}:latest"
        docker tag ${image} ${image_name}:latest
    done
}

tag_latest