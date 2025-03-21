#!/bin/bash

. ./configure.sh

python3 keycloak/keycloak-import.py      \
    --url "${KEYCLOAK_ADDR}"            \
    --username "admin"                  \
    --password "${PASSWORD_KEYCLOAK}"   \
    --fname "./keycloak/realm-export.json" \
    --client-name "${KEYCLOAK_USERNAME}"      \
    --client-password "${KEYCLOAK_PASSWORD}"
