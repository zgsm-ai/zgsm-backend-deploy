#!/bin/sh

. ./configure.sh

# chatgpt RESTful API port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
   "id": "chatgpt",
   "nodes": {
     "chatgpt:5000": 1
   },
   "type": "roundrobin"
 }'

# chatgpt WebSocket port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "websocket",
    "nodes": {
      "chatgpt:8765": 1
    },
    "type": "roundrobin"
  }'

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
