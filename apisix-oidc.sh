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


# 需要登录的接口，添加以下两个插件：
# openid-connect 和
# "openid-connect": {
#        "bearer_only": true,
#        "client_id": "$client_id",
#        "client_secret": "$client_secret",
#        "discovery": "http://第三方认证地址/dex/.well-known/openid-configuration",
#        "scope": "openid email profile",
#        "realm": "'"$KEYCLOAK_REALM"'",
#        "set_userinfo_header": true,
#        "ssl_verify": false
#      }
#       "response-rewrite": {
#         "headers": {
#             "set": {
#                   "Location": "http://apisix地址/login/vscode"
#               }
#           },
#           "status_code": 302,
#           "vars":[
#               [ "status","==",401]
#           ]
#       }


# 登录接口，这里 "bearer_only": false，允许重定向到登录页面；其余为true，不允许重定向，只做校验。
# 其余接口如果登录失败，401，重定向到接口。
# 这里核心插件为两个： openid-connect 和 redirect。openid-connect 用于认证拿到token，redirect用于将token传递到ide。
curl -i http://$APISIX_ADDR/apisix/admin/routes/realms-redirect \
  -H "$AUTH" \
  -H "$TYPE" \
  -X PUT \
  -d '
{
    "uris": [
        "/realms/*",
        "/login/vscode",
        "/login/oidc"
    ],
    "id": "realms-redirect",
    "name": "login-vscode",
    "plugins": {
      "openid-connect": {
        "bearer_only": false,
        "client_id": "'"$OIDC_CLIENT_ID"'",
        "client_secret": "'"$OIDC_CLIENT_SECRET"'",
        "discovery": "'"http://$OIDC_HOST:$OIDC_PORT""$OIDC_BASE_URL"'/.well-known/openid-configuration",
        "redirect_uri": "'"http://$ZGSM_BACKEND:$PORT_APISIX_ENTRY"'/login/oidc",
        "scope": "openid email profile",
        "session": {
          "secret": "zgsm-oidc-secret"
        },
        "force_reauthorize": false,
        "set_userinfo_header": false,
        "ssl_verify": false,
        "set_access_token_header": true,
        "access_token_in_authorization_header": false,
        "set_id_token_header": false,
        "renew_access_token_on_expiry": true,
        "refresh_session_interval": 900,
        "access_token_expires_leeway": 600
      },
     "redirect": {
            "uri": "vscode://zgsm-ai.zgsm/callback?token=${http_x_access_token}",
            "ret_code": 302
        },
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
     },
    "upstream": {
        "type": "roundrobin",
        "nodes": {
            "localhost:80": 1
        }
    }
}'
