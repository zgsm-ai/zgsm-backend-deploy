#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "copilot",
    "nodes": {
      "'"fauxpilot:$PORT_FAUXPILOT_INTERNAL"'": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/v1/completions", "/v2/completions", "/copilot_internal/*", "/v2/engines/*", "/v1/engines/*"],
    "id": "copilot",
    "name": "copilot",
    "upstream_id": "copilot",
    "plugins": {
      "openid-connect": {
        "client_id": "'"$CASDOOR_CLIENT_ID"'",
        "client_secret": "'"$CASDOOR_CLIENT_SECRET"'",
        "discovery": "'"http://$CASDOOR_HOST:$CASDOOR_PORT/.well-known/openid-configuration"'",
        "introspection_endpoint": "'"http://$CASDOOR_HOST:$CASDOOR_PORT/api/login/oauth/introspect"'",
        "bearer_only": true,
        "introspection_endpoint_auth_method": "client_secret_basic"
      },
      "response-rewrite": {
          "headers": {
              "set": {
                    "Location": "'"http://apisix:$PORT_APISIX_ENTRY"'/oidc_auth/plugin/login"
                }
            },
            "status_code": 302,
            "vars":[ [ "status","==",401] ]
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
