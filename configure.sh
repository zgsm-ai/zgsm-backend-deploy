#!/bin/sh

#-------------------------------------------------------------------------------
# 以下端口设置如非必要，请勿修改
#-------------------------------------------------------------------------------
PORT_APISIX_API="9180"
PORT_APISIX_ENTRY="9080"
PORT_APISIX_PROMETHEUS="9091"
PORT_APISIX_CONTROL="9092"
PORT_APISIX_DASHBOARD="9093"
PORT_ETCD="2379"
PORT_REDIS="6379"
PORT_POSTGRES="5432"
PORT_WEAVIATE="5003"
PORT_PORTAL="9081"
PORT_CHATGPT_API="5000"
PORT_CHATGPT_WS="8765"
PORT_COMPLETION="5001"
PORT_COMPLETION_INTERNAL="5000"
PORT_PROMETHEUS="9090"
PORT_GRAFANA="3000"
PORT_ES="9200"
PORT_AI_GATEWAY="8080"
PORT_HIGRESS_CONTROL="8001"
PORT_QUOTA_MANAGER="9001"
PORT_CREDIT_MANAGER="5173"
PORT_ISSUE_MANAGER="9003"
PORT_REVIEW_MANAGER="9004"
PORT_REVIEW_CHECKER="9005"
PORT_OIDC_AUTH="9006"
PORT_CHAT_RAG="9007"
PORT_CODEBASE_INDEXER="9008"
PORT_CASDOOR="9009"
PORT_COTUN="9010"
PORT_TUNNEL_MANAGER="9011"

#---------------------------------------------------------
# 私有镜像仓库设置
# 用户可以私有化部署镜像仓库，用于存放诸葛神码所使用的所有镜像
# 这些镜像默认存储在docker.io/zgsm下
#---------------------------------------------------------
# 私有镜像仓库的主机名
DH_HOST="docker.io"
# 私有镜像仓库中存储诸葛神码镜像的项目地址
DH_ADDR="docker.io/zgsm"

#---------------------------------------------------------
# 登录神码内部应用所使用的账号密码
# 建议修改，以提高系统安全性
#---------------------------------------------------------
# apisix中admin用户的APIKEY
APIKEY_APISIX_ADMIN="edd1c9f034335f136f87ad84b625c8f1"
# apisix中viewer用户的APIKEY
APIKEY_APISIX_VIEWER="4054f730f8e344346cd3f287985e76a2"
# apisix-dashboard的登录密码
PASSWORD_APISIX_DASHBOARD="sf2025~SHENMA"
# etcd的访问密码
PASSWORD_ETCD="sf2025~SHENMA"
# redis的访问密码
PASSWORD_REDIS="sf2025~SHENMA"
# postgres的访问密码
PASSWORD_POSTGRES="sf2025~SHENMA"
# elasticsearch的访问密码
PASSWORD_ELASTIC="4c6y4g6Z09T2w33pYRNKE3LG"

#---------------------------------------------------------
# 大模型相关设置，请根据实际部署情况设置
#---------------------------------------------------------
# 对话默认使用的模型名称
CHAT_DEFAULT_MODEL="deepseek-chat"
CHAT_API_KEY="966c3157fe65461dbc731cd540b6cd5d"
CHAT_AIGW_ADDR="http://higress:8080/v1/chat/completions"

# 代码补全模型的URL
CODE_COMPLETION_MODEL_HOST="http://172.16.254.5:32081/v1/completions"
# 代码补全采用的模型名称
CODE_COMPLETION_MODEL="DeepSeek-Coder-V2-Lite-Base"
# 代码补全模型的API-KEY
CODE_COMPLETION_MODEL_API_KEY="966c3157fe65461dbc731cd540b6cd5d"

#---------------------------------------------------------
# apisix设置，无需修改
#---------------------------------------------------------

APISIX_ADDR="127.0.0.1:${PORT_APISIX_API}"
AUTH="X-API-KEY: ${APIKEY_APISIX_ADMIN}"
TYPE="Content-Type: application/json"

#---------------------------------------------------------
# postgres/redis设置，无需修改
#---------------------------------------------------------
POSTGRES_USER="zgsm"
POSTGRES_DB="zgsm"

PGSQL_ADDR="postgres:${PORT_POSTGRES}"
REDIS_ADDR="redis:${PORT_REDIS}"

#---------------------------------------------------------
# 认证设置(oidc-auth/casdoor)，无需修改
#---------------------------------------------------------
# oidc-auth模块在casdoor中注册用的clientid
OIDC_AUTH_CLIENT_ID="9e2fc5d4fbcd52ef4f6f"
# oidc-auth模块在casdoor中注册用的client secret
OIDC_AUTH_CLIENT_SECRET="ab5d8ba28b0e6c0d6e971247cdc1deb269c9eea3"

# apisix使用OIDC协议与casdoor通讯验证请求者身份
OIDC_CLIENT_ID="9e2fc5d4fbcd52ef4f6f"
OIDC_CLIENT_SECRET="ab5d8ba28b0e6c0d6e971247cdc1deb269c9eea3"
# OIDC_CLIENT_ID="7c51a6b92dfebfa55d96"
# OIDC_CLIENT_SECRET="bcb3dc222a07fad21aabdd5035dadba2f09e05d6"
OIDC_CASDOOR_ADDR="http://casdoor:8000"
OIDC_DISCOVERY_ADDR="${OIDC_CASDOOR_ADDR}/.well-known/openid-configuration"
OIDC_INTROSPECTION_ENDPOINT="${OIDC_CASDOOR_ADDR}/api/login/oauth/introspect"
OIDC_TOKEN_ENDPOINT=""

#-------------------------------------------------------------------------------
#   以下设置请根据部署环境信息进行修改
#-------------------------------------------------------------------------------
# VSCODE扩展连接诸葛神码后端时使用的入口URL地址
# 一般会利用DNS及应用发布设备将该地址映射到 http://${COSTRICT_BACKEND}:${PORT_APISIX_ENTRY}
# 诸葛神码后端的IP地址，deploy.sh可自动获取
COSTRICT_BACKEND="172.16.0.4"
COSTRICT_BACKEND_BASEURL="http://${COSTRICT_BACKEND}:${PORT_APISIX_ENTRY}"
