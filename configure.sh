#!/bin/sh

#-------------------------------------------------------------------------------
#   以下设置请根据部署环境信息进行修改
#-------------------------------------------------------------------------------
# 诸葛神码后端的URL地址，一般会采用应用发布设备映射到 http://${ZGSM_BACKEND}:${PORT_APISIX_ENTRY}
ZGSM_ADDR="https://zgsm.sangfor.com"
# 诸葛神码后端的IP地址
ZGSM_BACKEND="172.16.0.4"

DH_HOST="harbor.sangfor.com"
DH_ADDR="harbor.sangfor.com/zgsm"

# apisix中admin用户的APIKEY
APIKEY_APISIX_ADMIN="edd1c9f034335f136f87ad84b625c8f1"
#
APIKEY_APISIX_VIEWER="4054f730f8e344346cd3f287985e76a2"
PASSWORD_APISIX_DASHBOARD="sf2025~SHENMA"
PASSWORD_ETCD="sf2025~SHENMA"
PASSWORD_REDIS="sf2025~SHENMA"
PASSWORD_POSTGRES="sf2025~SHENMA"
PASSWORD_ES="sf2025~SHENMA"
PASSWORD_ELASTIC="4c6y4g6Z09T2w33pYRNKE3LG"

# ES
ENROLLMENT_TOKEN="4c6y4g6Z09T2w33pYRNKE3LG"

# 对话模型
CHAT_MODEL="deepseek-chat"
# 补全模型
CODE_COMPLETION_MODEL_HOST="http://172.16.254.5:32081/v1/completions"
CODE_COMPLETION_MODEL="DeepSeek-Coder-V2-Lite-Base"
CODE_COMPLETION_MODEL_API_KEY="966c3157fe65461dbc731cd540b6cd5d"

#-------------------------------------------------------------------------------
# 以下设置如非必要，请勿修改
#-------------------------------------------------------------------------------
PORT_APISIX_API="9180"
PORT_APISIX_ENTRY="9080"
PORT_APISIX_PROMETHEUS="9091"
PORT_APISIX_CONTROL="9092"
PORT_APISIX_DASHBOARD="9000"
PORT_ETCD="2379"
PORT_REDIS="6379"
PORT_POSTGRES="5432"
PORT_PORTAL="9081"
PORT_CHATGPT_API="5000"
PORT_CHATGPT_WS="8765"
PORT_COMPLETION="5001"
PORT_COMPLETION_INTERNAL="5000"
PORT_PROMETHEUS="9090"
PORT_GRAFANA="3000"
PORT_ES="9200"
PORT_AI_GATEWAY="9000"
PORT_HIGRESS_CONTROL="9081"
PORT_QUOTA_MANAGER="9001"
PORT_CREDIT_MANAGER="5173"
PORT_ISSUE_MANAGER="9003"
PORT_REVIEW_MANAGER="9004"
PORT_REVIEW_CHECKER="9005"
PORT_OIDC_AUTH="9006"
PORT_CHAT_RAG="9007"
PORT_CODEBASE_INDEXER="9008"
PORT_CASDOOR="9009"

APISIX_ADDR="127.0.0.1:${PORT_APISIX_API}"
AUTH="X-API-KEY: ${APIKEY_APISIX_ADMIN}"
TYPE="Content-Type: application/json"

# postgres
POSTGRES_USER="zgsm"
POSTGRES_DB="zgsm"

PGSQL_ADDR="postgres:${PORT_POSTGRES}"
REDIS_ADDR="redis:${PORT_REDIS}"
AIGW_CHAT_ADDR="http://higress:${PORT_AI_GATEWAY}/v1/chat/completions"

# oidc-auth模块在casdoor中注册用的clientid
OIDC_AUTH_CLIENT_ID="9e2fc5d4fbcd52ef4f6f"
# oidc-auth模块在casdoor中注册用的client secret
OIDC_AUTH_CLIENT_SECRET="ab5d8ba28b0e6c0d6e971247cdc1deb269c9eea3"

# apisix使用OIDC协议与casdoor通讯验证请求者身份
OIDC_CLIENT_ID="7c51a6b92dfebfa55d96"
OIDC_CLIENT_SECRET="bcb3dc222a07fad21aabdd5035dadba2f09e05d6"
OIDC_CASDOOR_ADDR="http://casdoor:${PORT_CASDOOR}"
OIDC_DISCOVERY_ADDR="${OIDC_CASDOOR_ADDR}/.well-known/openid-configuration"
OIDC_INTROSPECTION_ENDPOINT="${OIDC_CASDOOR_ADDR}/api/login/oauth/introspect"
OIDC_TOKEN_ENDPOINT=""
