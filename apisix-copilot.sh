#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "copilot",
    "nodes": {
      "'"$ZGSM_BACKEND:$PORT_FAUXPILOT"'": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/v1/completions", "/v2/completions", "/copilot_internal/*", "/v2/engines/*", "/v1/engines/*"],
    "id": "copilot",
    "upstream_id": "copilot",
    "plugins": {
      "openid-connect": {
        "client_id": "'"$KEYCLOAK_CLIENT_ID"'",
        "client_secret": "'"$KEYCLOAK_CLIENT_SECRET"'",
        "discovery": "'"$KEYCLOAK_ADDR"'/realms/'"$KEYCLOAK_REALM"'/.well-known/openid-configuration",
        "introspection_endpoint_auth_method": "client_secret_basic",
        "realm": "'"$KEYCLOAK_REALM"'",
        "bearer_only": true,
        "ssl_verify": false
      },
      "limit-req": {
        "rate": 1,
        "burst": 1,
        "rejected_code": 503,
        "key_type": "var",
        "key": "remote_addr"
      },
      "limit-count": {
        "count": 10000,
        "time_window": 86400,
        "rejected_code": 429,
        "key": "remote_addr"
      },
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'
