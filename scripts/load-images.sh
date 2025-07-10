#!/bin/bash

# 本脚本运行的前提条件：
#   1. linux机器
#   2. 安装了docker
#

LOAD_DIR="./images"

function usage() {
    echo "usage: load-images.sh [options]"
    echo "  load SHENMA images from <LOAD_DIR>"
    echo "options:"
    echo "  [-l <LOAD_DIR>] - 从该目录加载镜像"
    echo "examples:"
    echo "  load-images.sh -l ./images"
}

while getopts "l:h" opt
do
    case $opt in
    l)
        LOAD_DIR=$OPTARG
        ;;
    ?)
        usage
        exit 1;;
    esac
done

echo LOAD_DIR = ${LOAD_DIR}

function load_images() {
    for image in `ls "${LOAD_DIR}"/*.tar`; do
        if [ ! -f ${image} ]; then
            continue
        fi
        echo "docker load -i ${image}"
        docker load -i ${image}
    done
}

load_images
