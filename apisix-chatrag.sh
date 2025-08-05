#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "chat-rag",
    "nodes": {
      "chat-rag:8888": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/chat-rag/api/v1/chat/*"],
    "id": "chat-rag",
    "name": "chat-rag-api",
    "upstream_id": "chat-rag",
    "plugins": {
      "request-id": {
        "include_in_response": true
      },
      "file-logger": {
        "include_req_body": true,
        "include_resp_body": true,
        "path": "logs/access.log"
      },
      "limit-count": {
        "count": 10000,
        "time_window": 86400,
        "rejected_code": 429,
        "key": "$remote_addr $http_x_forwarded_for",
        "key_type": "var_combination"
      },
      "limit-req": {
        "rate": 300,
        "burst": 300,
        "rejected_code": 429,
        "key_type": "var_combination",
        "key": "$remote_addr $http_x_forwarded_for"
      },
      "loki-logger": {
        "endpoint_addrs": ["http://loki.loki:3100"],
        "endpoint_uri": "/loki/api/v1/push",
        "include_req_body": true,
        "include_resp_body": true,
        "log_labels": {"job": "apisix"}
      },
      "openid-connect": {
        "client_id": "'"$OIDC_CLIENT_ID"'",
        "client_secret": "'"$OIDC_CLIENT_SECRET"'",
        "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
        "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
        "introspection_endpoint_auth_method": "client_secret_basic",
        "introspection_interval": 60,
        "bearer_only": true,
        "set_userinfo_header": true,
        "ssl_verify": false,
        "scope": "openid profile email"
      }
    }
  }'
