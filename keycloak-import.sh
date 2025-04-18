#!/bin/bash

. ./configure.sh


# 定义最大等待时间（秒，0 表示无限等待）
MAX_WAIT=0
echo "正在检查 keycloak 服务状态..."
start_time=$(date +%s)
while : ; do
  # 通过检测端口是否监听判断服务状态
  if curl -sSf "${KEYCLOAK_ADDR}" >/dev/null; then
    echo "keycloak 已成功启动!"
    break
  fi

  # 超时检测
  if [ $MAX_WAIT -ne 0 ]; then
    current_time=$(date +%s)
    if (( current_time - start_time > MAX_WAIT )); then
      echo "错误：在 ${MAX_WAIT} 秒内未检测到 keycloak 启动"
      exit 1
    fi
  fi

  echo "等待 keycloak ${KEYCLOAK_ADDR} 启动...（已等待 $(( $(date +%s) - start_time )) 秒）"
  sleep 5
done



python3 keycloak/keycloak-import.py      \
    --url "${KEYCLOAK_ADDR}"            \
    --username "admin"                  \
    --password "${PASSWORD_KEYCLOAK}"   \
    --fname "./keycloak/realm-export.json" \
    --client-name "${KEYCLOAK_USERNAME}"      \
    --client-password "${KEYCLOAK_PASSWORD}"
