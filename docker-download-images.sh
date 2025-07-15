#!/bin/sh

. ./configure.sh

# 检查images.list是否存在
if [ ! -f "scripts/images.list" ]; then
    echo "images.list不存在，生成新的镜像列表..."
    bash scripts/get-images-list.sh -o scripts/images.list
else
    echo "使用现有的images.list"
fi

# 验证镜像是否存在
echo "验证镜像..."
bash scripts/verify-images.sh -f scripts/images.list
status=$?

# 根据验证结果决定是否拉取镜像
if [ $status -eq 0 ]; then
    echo "所有镜像已存在，跳过拉取"
    exit 0
else
    echo "部分镜像不存在，开始拉取..."
    bash scripts/pull-images.sh -f scripts/images.list
    bash scripts/verify-images.sh -f scripts/images.list
    exit $?
fi
