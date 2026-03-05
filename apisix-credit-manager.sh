#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "credit-manager",
    "nodes": {
      "credit-manager:80": 1
    },
    "type": "roundrobin"
}'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "credit-manager",
    "name": "credit-manager-routes",
    "uris": ["/credit/manager*"],
    "upstream_id": "credit-manager",
    "plugins": {
      "limit-req": {
        "rate": 300,
        "burst": 300,
        "rejected_code": 429,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      },
      "limit-count": {
        "count": 10000,
        "time_window": 86400,
        "rejected_code": 429,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      }
    }
}'