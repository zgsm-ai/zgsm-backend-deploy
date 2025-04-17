#!/bin/sh

PORT_APISIX_API="9180"
PORT_APISIX_ENTRY="9080"
PORT_APISIX_PROMETHEUS="9091"
PORT_APISIX_CONTROL="9092"
PORT_APISIX_DASHBOARD="9000"
PORT_ETCD="2379"
PORT_REDIS="6379"
PORT_POSTGRES="5432"
PORT_KEYCLOAK="8080"
PORT_PORTAL="9081"
PORT_TRAMPOLINE="9082"
PORT_CHATGPT_API="5000"
PORT_CHATGPT_WS="8765"
PORT_FAUXPILOT="5001"
PORT_PROMETHEUS="9090"
PORT_GRAFANA="3000"
PORT_ES="9200"

APIKEY_APISIX_ADMIN="edd1c9f034335f136f87ad84b625c8f1"
APIKEY_APISIX_VIEWER="4054f730f8e344346cd3f287985e76a2"

AUTH="X-API-KEY: ${APIKEY_APISIX_ADMIN}"
TYPE="Content-Type: application/json"

PASSWORD_APISIX_DASHBOARD="sf2025~SHENMA"
PASSWORD_ETCD="sf2025~SHENMA"
PASSWORD_REDIS="sf2025~SHENMA"
PASSWORD_POSTGRES="sf2025~SHENMA"
PASSWORD_ES="sf2025~SHENMA"
PASSWORD_KEYCLOAK="sf2025~SHENMA"
PASSWORD_ELASTIC="4c6y4g6Z09T2w33pYRNKE3LG"

# ES
ENROLLMENT_TOKEN="4c6y4g6Z09T2w33pYRNKE3LG"

ZGSM_BACKEND="172.22.108.123"
APISIX_ADDR="${ZGSM_BACKEND}:${PORT_APISIX_API}"

KEYCLOAK_ADDR="http://${ZGSM_BACKEND}:${PORT_KEYCLOAK}"
KEYCLOAK_CLIENT_ID="vscode"
KEYCLOAK_CLIENT_SECRET="jFWyVy9wUKKSkX55TDBt2SuQWl7fDM1l"
KEYCLOAK_REALM="gw"
KEYCLOAK_USERNAME="zgsm"
KEYCLOAK_PASSWORD="123"

OPENAI_MODEL_HOST="http://one-api:30000/v1/completions"
OPENAI_MODEL="deepseek-chat"
OPENAI_MODEL_API_KEY="966c3157fe65461dbc731cd540b6cd5d"

CHAT_MODEL="deepseek-chat"

 # root key
ONE_API_INITIAL_ROOT_KEY="966c3157fe65461dbc731cd540b6cd5d"
# 用户认证token，不要超过32位
ONE_API_INITIAL_ROOT_ACCESS_TOKEN="e9e3-4cd3-abfc-36707f44ee1e"
ONE_API_PORT=30000