#!/bin/sh

. ./configure.sh

# cotun WebSocket port
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "cotun-websocket",
    "nodes": {
      "cotun.costrict.svc.cluster.local:8080": 1
    },
    "type": "roundrobin"
  }'

curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/ws", "/ws/*"],
    "id": "cotun-ws",
    "upstream_id": "cotun-websocket",
    "enable_websocket": true,
    "plugins": {
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
    }
  }'
