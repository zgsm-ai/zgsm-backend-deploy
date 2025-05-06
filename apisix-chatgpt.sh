#!/bin/sh

. ./configure.sh
. ./utils.sh

echo "Checking APISIX service status..."
retry "curl -sSf http://$APISIX_ADDR/apisix/admin/routes -H '$AUTH' -H '$TYPE' >/dev/null" 120 5 || fatal "Waiting for APISIX start-up completion timed out"
echo "APISIX has started successfully (Admin API response normal)"

# chatgpt RESTful API port
#curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
#    "id": "chatgpt",
#    "nodes": {
#      "'"chatgpt:$PORT_CHATGPT_API"'": 1
#    },
#    "type": "roundrobin"
#  }'

# chatgpt WebSocket port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "websocket",
    "nodes": {
      "'"chatgpt:$PORT_CHATGPT_WS"'": 1
    },
    "type": "roundrobin"
  }'

#curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#    "uris": ["/chat/*", "/answer", "/answer/*"],
#    "id": "chatgpt-qa",
#    "upstream_id": "chatgpt",
#    "plugins": {
#      "limit-req": {
#        "rate": 1,
#        "burst": 1,
#        "rejected_code": 503,
#        "key_type": "var",
#        "key": "remote_addr"
#      },
#      "limit-count": {
#        "count": 10000,
#        "time_window": 86400,
#        "rejected_code": 429,
#        "key": "remote_addr"
#      },
#      "file-logger": {
#        "path": "logs/access.log",
#        "include_req_body": true,
#        "include_resp_body": true
#      }
#    }
#  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/api/*"],
    "id": "chatgpt-api",
    "name": "chatgpt-api",
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
