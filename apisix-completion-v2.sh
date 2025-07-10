#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "code-completion",
    "nodes": {
      "code-completion:5000": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/code-completion/api/v1/completions"],
    "id": "code-completion",
    "upstream_id": "code-completion",
    "plugins": {
      "openid-connect": {
        "client_id": "'"$OIDC_CLIENT_ID"'",
        "client_secret": "'"$OIDC_CLIENT_SECRET"'",
        "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
        "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
        "introspection_endpoint_auth_method": "client_secret_basic",
        "bearer_only": true,
        "ssl_verify": false
      },
      "limit-req": {
        "rate": 10,
        "burst": 10,
        "rejected_code": 503,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      },
      "limit-count": {
        "count": 10000,
        "time_window": 86400,
        "rejected_code": 429,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      },
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'
