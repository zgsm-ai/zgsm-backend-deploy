#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "oidc-auth",
    "nodes": {
      "oidc-auth:8080": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
  "id": "oidc-auth",
  "name": "oidc-auth-routes",
  "uris": [
    "/oidc-auth/api/v1/plugin*",
    "/oidc-auth/api/v1/manager*"
  ],
  "upstream_id": "oidc-auth"
}'
