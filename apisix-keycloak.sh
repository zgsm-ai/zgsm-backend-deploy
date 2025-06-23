#!/bin/sh

. ./configure.sh

#
# Four upstreams:
#   keycloak - overall login logic
#   portal - login page resources
#   trampoline - login success redirection
#   kaptcha - graphical verification code
#

# Define upstream for login-related page resources
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "portal",
    "nodes": {
        "'"portal:$PORT_PORTAL_INTERNAL"'": 1
    },
    "type": "roundrobin"
}'

# Service for generating verification code images
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "kaptcha",
    "nodes": {
        "'"http://$CASDOOR_HOST:$CASDOOR_PORT"'": 1
    },
    "type": "roundrobin"
}'

# Define upstream for credit managermant page resource
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "credit-manager",
    "nodes": {
        "'"$CREDIT_MANAGER_HOST:$CREDIT_MANAGER_PORT"'": 1
    },
    "type": "roundrobin"
}'

# Resources used by login pages
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/login/css/*", "/login/cdn/*", "/login/img/*", "/login/resources/*"],
    "id": "keycloak-portal-resources",
    "upstream_id": "portal"
  }'

# Images needed for login page: img/keycloak-bg.png, img/favicon.ico, css/login.css
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/resources/*"],
    "vars": [
      [ "uri", "~*", "^/resources/.*/login/phone/.*$" ]
    ],
    "id": "keycloak-login-resource",
    "upstream_id": "portal",
    "plugins": {
      "proxy-rewrite": {
        "regex_uri": ["^/resources/.*/login/phone/(.*)", "/login/$1"]
      }
    }
  }'

# Generate verification code
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/realms/'"$KEYCLOAK_REALM"'/captcha/code"],
    "id": "keycloak-captcha",
    "upstream_id": "kaptcha",
    "plugins": {
      "proxy-rewrite": {
        "uri": "/codeByBase64"
      }
    }
  }'

# credit managerment page
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/credit/manager*"],
    "id": "credit-manager",
    "upstream_id": "credit-manager",
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
                    "Location": "'"http://apisix:$PORT_APISIX_ENTRY"'/login/vscode"
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



# Define keycloak endpoint
# curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
#     "id": "keycloak",
#     "nodes": {
#         "'"keycloak:$PORT_KEYCLOAK_INTERNAL"'": 1
#     },
#     "type": "roundrobin"
# }'

# trampoline: login success redirection (URL: /login/ok), responsible for launching vscode
# curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
#     "id": "trampoline",
#     "nodes": {
#         "'"trampoline:$PORT_TRAMPOLINE_INTERNAL"'": 1
#     },
#     "type": "roundrobin"
# }'

# Direct requests to keycloak to the keycloak endpoint
# curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#     "uris": ["/realms/'"$KEYCLOAK_REALM"'/*"],
#     "id": "keycloak",
#     "upstream_id": "keycloak"
#   }'

# Direct requests to keycloak to the keycloak endpoint
# curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#     "uris": ["/resources/*"],
#     "vars": [
#       [ "uri", "!", "~*", "^/resources/.*/login/phone/.*$" ]
#     ],
#     "id": "keycloak-common-resource",
#     "upstream_id": "keycloak"
#   }'

# Forward successful login redirection requests to trampoline service, "uris": ["/login/ok", "/login/resources/*"]
# curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
#     "uris": ["/login/ok"],
#     "id": "keycloak-trampoline",
#     "upstream_id": "trampoline"
#   }'
