#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "casdoor",
    "nodes": {
      "casdoor:8000": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
  "uris": [
    "/login/oauth/*",
    "/api/login/oauth/*",
    "/casdoor/*",
    "/static/*",
    "/api/get-app-login*",
    "/api/get-account*",
    "/api/get-application*",
    "/api/get-captcha*",
    "/api/send-verification-code*",
    "/api/login*",
    "/login/success",
    "/callback*"
  ],
  "id": "casdoor",
  "name": "casdoor-routes",
  "upstream_id": "casdoor"
}'
