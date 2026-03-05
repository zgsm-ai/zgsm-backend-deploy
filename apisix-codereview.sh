#!/bin/sh

. ./configure.sh

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "review-manager",
    "nodes": {
      "review-manager:8080": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "issue-manager",
    "nodes": {
      "issue-manager:8080": 1
    },
    "type": "roundrobin"
  }'

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "id": "review-manager",
    "name": "review-manager-api",
    "uris": ["/review-manager/*"],
    "upstream_id": "review-manager",
    "plugins": {
      "openid-connect": {
         "client_id": "'"$OIDC_CLIENT_ID"'",
         "client_secret": "'"$OIDC_CLIENT_SECRET"'",
         "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
         "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
         "introspection_endpoint_auth_method": "client_secret_basic",
         "bearer_only": true,
         "set_userinfo_header": true,
         "set_id_token_header": false,
         "ssl_verify": false
       },
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

curl -i http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uri": "/issue-manager/*",
    "id": "issue-manager-api",
    "name": "issue-manager-api",
    "upstream_id": "issue-manager",
    "plugins": {
      "openid-connect": {
         "client_id": "'"$OIDC_CLIENT_ID"'",
         "client_secret": "'"$OIDC_CLIENT_SECRET"'",
         "discovery": "'"$OIDC_DISCOVERY_ADDR"'",
         "introspection_endpoint": "'"$OIDC_INTROSPECTION_ENDPOINT"'",
         "introspection_endpoint_auth_method": "client_secret_basic",
         "bearer_only": true,
         "set_userinfo_header": true,
         "set_id_token_header": false,
         "ssl_verify": false
       },
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