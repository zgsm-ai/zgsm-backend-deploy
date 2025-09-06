#!/bin/sh

. ./configure.sh

SERVICE_NAME="grafana"

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "grafana",
    "nodes": {
      "grafana:3000": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "grafana",
    "name": "grafana-api",
    "uris": ["/grafana/*"],
    "upstream_id": "grafana",
    "plugins": {
      "limit-req": {
        "rate": 10,
        "burst": 10,
        "rejected_code": 503,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      }
    }
  }'
