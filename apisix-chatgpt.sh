#!/bin/sh

. ./configure.sh

# Define the maximum waiting time (seconds, 0 means wait indefinitely)
MAX_WAIT=0
echo "Checking APISIX service status..."
start_time=$(date +%s)
while : ; do
  # Determine the service status by checking if the port is listening
  if curl -sSf http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" >/dev/null; then
    echo "APISIX started successfully (management interface responds normally)"
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

# RESTful API port for chatgpt
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "chatgpt",
    "nodes": {
      "'"$ZGSM_BACKEND:$PORT_CHATGPT_API"'": 1
    },
    "type": "roundrobin"
  }'

# WebSocket port for chatgpt
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "websocket",
    "nodes": {
      "'"$ZGSM_BACKEND:$PORT_CHATGPT_WS"'": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/chat/*", "/answer", "/answer/*"],
    "id": "chatgpt-qa",
    "upstream_id": "chatgpt",
    "plugins": {
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

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/api/*"],
    "id": "chatgpt-api",
    "upstream_id": "chatgpt",
    "plugins": {
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

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/socket.io/*"],
    "id": "chatgpt-ws",
    "upstream_id": "websocket",
    "enable_websocket": true,
    "plugins": {
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'
