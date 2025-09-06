#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "quota-manager",
    "nodes": {
      "quota-manager:8080": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "quota-manager",
    "name": "quota-manager",
    "uris": ["/quota-manager/api/v1/quota*"],
    "upstream_id": "quota-manager",
    "plugins": {
      "file-logger": {
        "include_req_body": true,
        "include_resp_body": true,
        "path": "logs/access.log"
      },
      "limit-count": {
        "allow_degradation": false,
        "count": 10000,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for",
        "policy": "local",
        "rejected_code": 429,
        "show_limit_quota_header": true,
        "time_window": 86400
      },
      "limit-req": {
        "allow_degradation": false,
        "burst": 300,
        "key": "$remote_addr $http_x_forwarded_for",
        "key_type": "var_combination",
        "nodelay": false,
        "policy": "local",
        "rate": 300,
        "rejected_code": 429
      },
      "openid-connect": {
        "client_id": "'"$OIDC_CLIENT_ID"'",
        "client_secret": "'"$OIDC_CLIENT_SECRET"'",
        "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
        "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
        "introspection_endpoint_auth_method": "client_secret_basic",
        "introspection_interval": 60,
        "bearer_only": true,
        "scope": "openid profile email"
      }
    }
  }'

