#!/bin/sh

. ./configure.sh

curl -X POST http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -d @apisix-routes.json
curl -X POST http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -d @apisix-upstreams.json
