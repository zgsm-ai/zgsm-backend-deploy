#!/bin/sh

. ./configure.sh

#
# Submit issue report, page resources are hosted on the portal service, and the API '/api/feedbacks/issue' is implemented by chatgpt.
#

# Define the upstream for storing login-related page resources
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "portal",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_PORTAL"'": 1
    },
    "type": "roundrobin"
}'

# Resources used for login pages
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/issue/*"],
    "id": "issue-resources",
    "upstream_id": "portal"
  }'
