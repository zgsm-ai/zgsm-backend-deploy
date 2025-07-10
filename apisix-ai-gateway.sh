#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "ai-gateway",
    "nodes": {
      "higress-gateway:80": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": [
      "/ai-gateway/api/v1/models"
    ],
    "id": "ai-gateway",
    "name": "ai-gateway",
    "upstream_id": "ai-gateway",
    "status": 1
  }'
