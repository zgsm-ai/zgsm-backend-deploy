#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
  "id": "codebase-embedder",
  "uris": [
    "/codebase-embedder/api/v1/files/token",
    "/codebase-embedder/api/v1/files/upload",
    "/codebase-embedder/api/v1/files/status",
    "/codebase-embedder/api/v1/embeddings"
  ],
  "name": "codebase-embedder",
  "upstream": {
    "nodes": [
      {
        "host": "codebase-embedder",
        "port": 8888,
        "weight": 1 
      }
    ],
    "type": "roundrobin",
    "scheme": "http",
    "pass_host": "pass"
  },
  "plugins": {
    "openid-connect": { 
      "client_id": "'"$OIDC_CLIENT_ID"'",
      "client_secret": "'"$OIDC_CLIENT_SECRET"'",
      "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
      "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
      "introspection_endpoint_auth_method": "client_secret_basic",
      "introspection_interval": 60,
      "bearer_only": true,
      "scope": "openid profile email",
      "set_access_token_header": true,
      "set_id_token_header": true,
      "set_userinfo_header": true,
      "ssl_verify": false
    }
  }
}'