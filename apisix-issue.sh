#!/bin/sh

. ./configure.sh

#
# 提交问题报告,页面资源托管在portal服务，API ‘/api/feedbacks/issue’ 由chatgpt实现。
#

# 定义存放登录相关页面资源的upstream
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "portal",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_PORTAL"'": 1
    },
    "type": "roundrobin"
}'

# 登录各页面用到的资源
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/issue/*"],
    "id": "issue-resources",
    "upstream_id": "portal"
  }'
