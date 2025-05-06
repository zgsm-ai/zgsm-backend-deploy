#!/bin/sh

. ./configure.sh

# Define maximum wait time (seconds, 0 means infinite wait)
MAX_WAIT=0
echo "Checking APISIX service status..."
start_time=$(date +%s)
while : ; do
  # Check service status by detecting if the port is listening
  if curl -sSf http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" >/dev/null; then
    echo "APISIX has started successfully (admin interface responds normally)"
    break
  fi

  # Timeout detection
  if [ $MAX_WAIT -ne 0 ]; then
    current_time=$(date +%s)
    if (( current_time - start_time > MAX_WAIT )); then
      echo "Error: APISIX startup not detected within ${MAX_WAIT} seconds"
      exit 1
    fi
  fi

  echo "Waiting for APISIX to start... (waited $(( $(date +%s) - start_time )) seconds)"
  sleep 5
done

# one-api RESTful API port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "one-api",
    "nodes": {
      "'"one-api:$ONE_API_PORT"'": 1
    },
    "type": "roundrobin"
  }'


curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/v1/chat/*", "/v1/models","/v1/embeddings"],
    "id": "one-api",
    "name": "one-api",
    "upstream_id": "one-api",
    "plugins": {
       "openid-connect": {
         "client_id": "'"$OIDC_CLIENT_ID"'",
         "client_secret": "'"$OIDC_CLIENT_SECRET"'",
         "discovery": "'"http://$OIDC_HOST:$OIDC_PORT""$OIDC_BASE_URL"'/.well-known/openid-configuration",
         "introspection_endpoint_auth_method": "client_secret_basic",
         "realm": "'"$KEYCLOAK_REALM"'",
         "bearer_only": true,
         "set_userinfo_header": true,
         "ssl_verify": false
       },
      "response-rewrite": {
          "headers": {
              "set": {
                    "Location": "'"http://apisix:$PORT_APISIX_ENTRY"'/login/vscode"
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
      },
      "proxy-rewrite": {
         "headers": {
          "Authorization": "'"Bearer ${ONE_API_INITIAL_ROOT_KEY}"'"
          }
      }
    }
  }'
