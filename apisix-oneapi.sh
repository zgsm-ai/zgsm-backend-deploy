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

# oneapi的RESTful API端口
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "one-api",
    "nodes": {
      "'"$ZGSM_BACKEND:$ONE_API_PORT"'": 1
    },
    "type": "roundrobin"
  }'


curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/v1/chat/*", "/v1/models","/v1/embeddings"],
    "id": "one-api",
    "name": "one-api",
    "upstream_id": "one-api",
    "plugins": {
       "openid-connect": {
         "client_id": "'"$OIDC_CLIENT_ID"'",
         "client_secret": "'"$OIDC_CLIENT_SECRET"'",
         "discovery": "'"http://$OIDC_HOST:$OIDC_PORT""$OIDC_BASE_URL"'/.well-known/openid-configuration",
         "introspection_endpoint_auth_method": "client_secret_basic",
         "realm": "'"$KEYCLOAK_REALM"'",
         "bearer_only": true,
         "set_userinfo_header": true,
         "ssl_verify": false
       },
      "response-rewrite": {
          "headers": {
              "set": {
                    "Location": "'"http://$ZGSM_BACKEND:$PORT_APISIX_ENTRY"'/login/vscode"
                }
            },
            "status_code": 302,
            "vars":[ [ "status","==",401] ]
        },
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
      },
      "proxy-rewrite": {
         "headers": {
          "Authorization": "'"Bearer ${ONE_API_INITIAL_ROOT_KEY}"'"
          }
      }
    }
  }'
