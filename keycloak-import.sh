#!/bin/bash

. ./configure.sh

python keycloak/keycloak-import.py      \
    --url "${KEYCLOAK_ADDR}"            \
    --username "admin"                  \
    --password "${PASSWORD_KEYCLOAK}"   \
    --fname "./keycloak/realm-export.json"
