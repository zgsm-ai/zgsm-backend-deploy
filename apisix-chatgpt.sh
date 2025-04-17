#!/bin/sh

. ./configure.sh

# 定义最大等待时间（秒，0 表示无限等待）
MAX_WAIT=0
echo "正在检查 APISIX 服务状态..."
start_time=$(date +%s)
while : ; do
  # 通过检测端口是否监听判断服务状态
  if curl -sSf http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" >/dev/null; then
    echo "APISIX 已成功启动（管理接口响应正常）"
    break
  fi

  # 超时检测
  if [ $MAX_WAIT -ne 0 ]; then
    current_time=$(date +%s)
    if (( current_time - start_time > MAX_WAIT )); then
      echo "错误：在 ${MAX_WAIT} 秒内未检测到 APISIX 启动"
      exit 1
    fi
  fi

  echo "等待 APISIX 启动...（已等待 $(( $(date +%s) - start_time )) 秒）"
  sleep 5
done

# chatgpt的RESTful API端口
#curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
#    "id": "chatgpt",
#    "nodes": {
#      "'"$ZGSM_BACKEND:$PORT_CHATGPT_API"'": 1
#    },
#    "type": "roundrobin"
#  }'

# chatgpt的WebSocket端口
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "websocket",
    "nodes": {
      "'"$ZGSM_BACKEND:$PORT_CHATGPT_WS"'": 1
    },
    "type": "roundrobin"
  }'

#curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#    "uris": ["/chat/*", "/answer", "/answer/*"],
#    "id": "chatgpt-qa",
#    "upstream_id": "chatgpt",
#    "plugins": {
#      "limit-req": {
#        "rate": 1,
#        "burst": 1,
#        "rejected_code": 503,
#        "key_type": "var",
#        "key": "remote_addr"
#      },
#      "limit-count": {
#        "count": 10000,
#        "time_window": 86400,
#        "rejected_code": 429,
#        "key": "remote_addr"
#      },
#      "file-logger": {
#        "path": "logs/access.log",
#        "include_req_body": true,
#        "include_resp_body": true
#      }
#    }
#  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/api/*"],
    "id": "chatgpt-api",
    "upstream_id": "chatgpt",
    "plugins": {
      "limit-req": {
        "rate": 1,
        "burst": 1,
        "rejected_code": 503,
        "key_type": "var",
        "key": "remote_addr"
      },
      "limit-count": {
        "count": 10000,
        "time_window": 86400,
        "rejected_code": 429,
        "key": "remote_addr"
      },
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/socket.io/*"],
    "id": "chatgpt-ws",
    "upstream_id": "websocket",
    "enable_websocket": true,
    "plugins": {
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'
