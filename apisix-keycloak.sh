#!/bin/sh

. ./configure.sh

#
# 四个上游：
#   keycloak-登录整体逻辑
#   portal-登录页面资源
#   trampoline-登录成功跳板
#   kaptcha-图形验证码
#

# 定义存放登录相关页面资源的upstream
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "portal",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_PORTAL"'": 1
    },
    "type": "roundrobin"
}'

# trampoline: 登录成功跳板(URL: /login/ok),负责拉起vscode
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "trampoline",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_TRAMPOLINE"'": 1
    },
    "type": "roundrobin"
}'

# 生成图片校验码的服务
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "kaptcha",
    "nodes": {
        "'"$ZGSM_BACKEND:9696"'": 1
    },
    "type": "roundrobin"
}'

# 定义keycloak这个端点
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "keycloak",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_KEYCLOAK"'": 1
    },
    "type": "roundrobin"
}'

# 把请求keycloak的请求定向到keycloak端点
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/realms/'"$KEYCLOAK_REALM"'/*"],
    "id": "keycloak",
    "upstream_id": "keycloak"
  }'

# 登录各页面用到的资源
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/login/css/*", "/login/cdn/*", "/login/img/*", "/login/resources/*"],
    "id": "keycloak-portal-resources",
    "upstream_id": "portal"
  }'

# 把请求keycloak的请求定向到keycloak端点
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/resources/*"],
    "vars": [
      [ "uri", "!", "~*", "^/resources/.*/login/phone/.*$" ]
    ],
    "id": "keycloak-common-resource",
    "upstream_id": "keycloak"
  }'

# 登录页需要用到的图片:img/keycloak-bg.png,img/favicon.ico,css/login.css
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/resources/*"],
    "vars": [
      [ "uri", "~*", "^/resources/.*/login/phone/.*$" ]
    ],
    "id": "keycloak-login-resource",
    "upstream_id": "portal",
    "plugins": {
      "proxy-rewrite": {
        "regex_uri": ["^/resources/.*/login/phone/(.*)", "/login/$1"]
      }
    }
  }'

# 将登录成功后的跳板请求转发给trampoline服务，"uris": ["/login/ok", "/login/resources/*"],
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/login/ok"],
    "id": "keycloak-trampoline",
    "upstream_id": "trampoline"
  }'

# 生成验证码
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/realms/'"$KEYCLOAK_REALM"'/captcha/code"],
    "id": "keycloak-captcha",
    "upstream_id": "kaptcha",
    "plugins": {
      "proxy-rewrite": {
        "uri": "/codeByBase64"
      }
    }
  }'
