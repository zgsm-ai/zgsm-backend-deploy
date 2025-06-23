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

# aigateway RESTful API port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "aigateway",
    "nodes": {
      "'"$AIGATEWAY_HOST:$AIGATEWAY_PORT"'": 1
    },
    "type": "roundrobin"
  }'


curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/v1/chat/*", "/v1/models","/v1/embeddings"],
    "id": "aigateway",
    "name": "aigateway",
    "upstream_id": "aigateway",
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


# curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#     "uris": ["/v1/chat/*", "/v1/models","/v1/embeddings"],
#     "id": "aigateway",
#     "name": "aigateway",
#     "upstream_id": "aigateway"
#   }'
