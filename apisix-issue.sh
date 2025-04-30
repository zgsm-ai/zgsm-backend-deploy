#!/bin/sh

. ./configure.sh

#
# Submit issue reports, page resources are hosted on the portal service, API '/api/feedbacks/issue' is implemented by chatgpt.
#

# Define upstream for login-related page resources
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "portal",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_PORTAL"'": 1
    },
    "type": "roundrobin"
}'

# Resources used by login pages
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/issue/*"],
    "id": "issue-resources",
    "upstream_id": "portal"
  }'
