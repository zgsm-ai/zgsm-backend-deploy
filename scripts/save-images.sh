#!/bin/bash

# 本脚本运行的前提条件：
#   1. linux机器
#   2. 安装了docker
#

IMAGE_LIST_FILE=""
IMAGE_LIST_STR=""
SAVE_DIR="./images"

function usage() {
    echo "usage: save-images.sh [options]"
    echo "  save SHENMA images to ./images"
    echo "options:"
    echo "  [-i <IMAGE_LIST_STR>] - 镜像列表,需将该列表中的所有镜像保存到指定的目录下"
    echo "  [-f <IMAGE_LIST_FILE>] - 镜像列表文件,需将把该文件中指定的镜像保存到指定目录下"
    echo "  [-s <SAVE_DIR>] - 将镜像保存到该目录下"
    echo "examples:"
    echo "  save-images.sh -f images.list -s ./v1-images"
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
    s)
        SAVE_DIR=$OPTARG
        ;;
    ?)
        usage
        exit 1;;
    esac
done

echo IMAGE_LIST_STR  = ${IMAGE_LIST_STR}
echo IMAGE_LIST_FILE = ${IMAGE_LIST_FILE}
echo SAVE_DIR = ${SAVE_DIR}

IMAGES="apache/apisix:3.9.1-debian
apache/apisix-dashboard:3.0.0-alpine
bitnami/etcd:3.5.14
docker.io/redis:7.2.4
postgres:15-alpine
docker.elastic.co/elasticsearch/elasticsearch:8.9.0
quay.io/keycloak/keycloak:20.0.5
nginx:1.27.1
docker.sangfor.com/containerd/chat-server:1.2.0
docker.sangfor.com/moyix/copilot_proxy:1.5.15
docker.io/justsong/one-api:latest
docker.elastic.co/kibana/kibana:8.9.0
docker.io/grafana/grafana:11.2.0
quay.io/prometheus/prometheus:v2.54.0
higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/all-in-one:latest
"

if [ "${IMAGE_LIST_STR}" != "" ]; then
    IMAGES="${IMAGE_LIST_STR}"
fi

if [ "${IMAGE_LIST_FILE}" != "" ]; then
    IMAGES=`cat ${IMAGE_LIST_FILE}`
fi

function save_images() {
    mkdir -p ${SAVE_DIR}
    for image in `echo ${IMAGES}`; do
        after_slash=${image##*/}
        fname=${after_slash//:/-}
        echo "docker save -o ${SAVE_DIR}/${fname}.tar ${image}"
        docker save -o ${SAVE_DIR}/${fname}.tar ${image}
    done
}

save_images
