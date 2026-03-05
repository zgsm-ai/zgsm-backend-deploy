#!/bin/sh

. ./configure.sh

curl http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X GET > api6-routes.json
curl http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X GET > api6-upstreams.json
