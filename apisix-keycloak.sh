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
        "'"$ZGSM_BACKEND:$PORT_PORTAL"'": 1
    },
    "type": "roundrobin"
}'

# trampoline: login success redirection (URL: /login/ok), responsible for launching vscode
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "trampoline",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_TRAMPOLINE"'": 1
    },
    "type": "roundrobin"
}'

# Service for generating verification code images
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "kaptcha",
    "nodes": {
        "'"$ZGSM_BACKEND:9696"'": 1
    },
    "type": "roundrobin"
}'

# Define keycloak endpoint
curl -i http://$APISIX_ADDR/apisix/admin/upstreams -H "$AUTH" -H "$TYPE" -X PUT  -d '{
    "id": "keycloak",
    "nodes": {
        "'"$ZGSM_BACKEND:$PORT_KEYCLOAK"'": 1
    },
    "type": "roundrobin"
}'

# Direct requests to keycloak to the keycloak endpoint
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/realms/'"$KEYCLOAK_REALM"'/*"],
    "id": "keycloak",
    "upstream_id": "keycloak"
  }'

# Resources used by login pages
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/login/css/*", "/login/cdn/*", "/login/img/*", "/login/resources/*"],
    "id": "keycloak-portal-resources",
    "upstream_id": "portal"
  }'

# Direct requests to keycloak to the keycloak endpoint
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/resources/*"],
    "vars": [
      [ "uri", "!", "~*", "^/resources/.*/login/phone/.*$" ]
    ],
    "id": "keycloak-common-resource",
    "upstream_id": "keycloak"
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

# Forward successful login redirection requests to trampoline service, "uris": ["/login/ok", "/login/resources/*"]
curl -i  http://$APISIX_ADDR/apisix/admin/routes -H "$AUTH" -H "$TYPE" -X PUT -d '{
    "uris": ["/login/ok"],
    "id": "keycloak-trampoline",
    "upstream_id": "trampoline"
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
