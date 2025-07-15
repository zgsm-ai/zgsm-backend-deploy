#!/bin/bash

# 本脚本运行的前提条件：
#   1. linux机器
#   2. 安装了docker
#

IMAGE_LIST_FILE=""
IMAGE_LIST_STR=""

function usage() {
    echo "usage: pull-images.sh [options]"
    echo "  pull SHENMA images"
    echo "options:"
    echo "  [-i <IMAGE_LIST_STR>] - 镜像列表,需将该列表中的所有镜像保存到指定的目录下"
    echo "  [-f <IMAGE_LIST_FILE>] - 镜像列表文件,需将把该文件中指定的镜像保存到指定目录下"
    echo "examples:"
    echo "  pull-images.sh -f images.list"
}

while getopts ":i:f:s:" opt
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

echo IMAGE_LIST_STR  = ${IMAGE_LIST_STR}
echo IMAGE_LIST_FILE = ${IMAGE_LIST_FILE}

IMAGES=""
if [ "${IMAGE_LIST_STR}" != "" ]; then
    IMAGES="${IMAGE_LIST_STR}"
fi

if [ "${IMAGE_LIST_FILE}" != "" ]; then
    IMAGES=`cat ${IMAGE_LIST_FILE}`
fi

function pull_images() {
    for image in `echo ${IMAGES}`; do
        echo "docker pull ${image}"
        docker pull ${image}
    done
}

pull_images
