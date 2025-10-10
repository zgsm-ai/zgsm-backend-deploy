#!/bin/bash

IMAGE_LIST_FILE=""
IMAGE_LIST_STR=""
MISSING_IMAGES=0

function usage() {
    echo "usage: verify-images.sh [options]"
    echo "  检查SHENMA镜像是否已拉取到本地"
    echo "options:"
    echo "  [-i <IMAGE_LIST_STR>] - 镜像列表字符串"
    echo "  [-f <IMAGE_LIST_FILE>] - 镜像列表文件"
    echo "examples:"
    echo "  verify-images.sh -f images.list"
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

function verify_images() {
    echo "开始检查镜像..."
    for image in `echo ${IMAGES}`; do
        image_id=$(docker images -q "${image}" 2> /dev/null)
        if [ -z "${image_id}" ]; then
            echo "[缺失] ${image}"
            MISSING_IMAGES=$((MISSING_IMAGES+1))
        else
            echo "[存在] ${image}"
        fi
    done
    
    if [ ${MISSING_IMAGES} -gt 0 ]; then
        echo "检查完成，共有 ${MISSING_IMAGES} 个镜像缺失"
        exit 1
    else
        echo "所有镜像已存在"
        exit 0
    fi
}

verify_images
