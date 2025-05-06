#!/bin/bash

. ./configure.sh
. ./utils.sh

echo "Checking Keycloak service status..."
retry "curl -sSf $KEYCLOAK_ADDR >/dev/null" 120 5 || fatal "Waiting for Keycloak start-up completion timed out"
echo "Keycloak has started successfully (Admin interface response normal)"

python3 keycloak/keycloak-import.py      \
    --url "${KEYCLOAK_ADDR}"            \
    --username "admin"                  \
    --password "${PASSWORD_KEYCLOAK}"   \
    --fname "./keycloak/realm-export.json" \
    --client-name "${KEYCLOAK_USERNAME}"      \
    --client-password "${KEYCLOAK_PASSWORD}"
