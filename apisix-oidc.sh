#!/bin/sh

set -x

. ./configure.sh

# Define maximum waiting time (seconds, 0 means infinite wait)
# MAX_WAIT=0
# echo "Checking APISIX service status..."
# start_time=$(date +%s)
# while : ; do
#   # Check service status by detecting if the port is listening
#   if curl -sSf http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" >/dev/null; then
#     echo "APISIX has been successfully started (admin interface responds normally)"
#     break
#   fi

#   # Timeout detection
#   if [ $MAX_WAIT -ne 0 ]; then
#     current_time=$(date +%s)
#     if (( current_time - start_time > MAX_WAIT )); then
#       echo "Error: APISIX startup not detected within ${MAX_WAIT} seconds"
#       exit 1
#     fi
#   fi

#   echo "Waiting for APISIX to start...(waited $(( $(date +%s) - start_time )) seconds)"
#   sleep 5
# done


# For interfaces requiring login, add the following two plugins:
# openid-connect and
# "openid-connect": {
#        "bearer_only": true,
#        "client_id": "$client_id",
#        "client_secret": "$client_secret",
#        "discovery": "http://third-party-auth-address/dex/.well-known/openid-configuration",
#        "scope": "openid email profile",
#        "realm": "'"$KEYCLOAK_REALM"'",
#        "set_userinfo_header": true,
#        "ssl_verify": false
#      }
#       "response-rewrite": {
#         "headers": {
#             "set": {
#                   "Location": "http://apisix-address/login/vscode"
#               }
#           },
#           "status_code": 302,
#           "vars":[
#               [ "status","==",401]
#           ]
#       }


# Login interface, here "bearer_only": false, allowing redirection to the login page; others are true, not allowing redirection, only for validation.
# Other interfaces will redirect to the interface if login fails with 401.
# The core plugins here are two: openid-connect and redirect. openid-connect is used for authentication to get the token, redirect is used to pass the token to the IDE.
curl -i http://$APISIX_ADDR/apisix/admin/routes/realms-redirect \
  -H "$AUTH" \
  -H "$TYPE" \
  -X PUT \
  -d '
{
    "uris": [
        "/realms/*",
        "/login/vscode",
        "/login/oidc"
    ],
    "id": "realms-redirect",
    "name": "login-vscode",
    "plugins": {
      "openid-connect": {
        "bearer_only": false,
        "client_id": "'"$CASDOOR_CLIENT_ID"'",
        "client_secret": "'"$CASDOOR_CLIENT_SECRET"'",
        "discovery": "'"http://$CASDOOR_HOST:$CASDOOR_PORT/.well-known/openid-configuration"',
        "redirect_uri": "'"http://apisix:$PORT_APISIX_ENTRY"'/login/oidc",
        "scope": "openid email profile",
        "session": {
          "secret": "zgsm-oidc-secret"
        },
        "force_reauthorize": false,
        "set_userinfo_header": false,
        "ssl_verify": false,
        "set_access_token_header": true,
        "access_token_in_authorization_header": false,
        "set_id_token_header": false,
        "renew_access_token_on_expiry": true,
        "refresh_session_interval": 900,
        "access_token_expires_leeway": 600
      },
     "redirect": {
            "uri": "vscode://zgsm-ai.zgsm/callback?token=${http_x_access_token}",
            "ret_code": 302
        },
      "file-logger": {
        "path": "logs/access.log",
        "include_req_body": true,
        "include_resp_body": true
      }
     },
    "upstream": {
        "type": "roundrobin",
        "nodes": {
            "localhost:80": 1
        }
    }
}'
