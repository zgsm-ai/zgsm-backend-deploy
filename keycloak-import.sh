#!/bin/bash

. ./configure.sh


# Define maximum wait time (seconds, 0 means infinite wait)
MAX_WAIT=0
echo "Checking keycloak service status..."
start_time=$(date +%s)
while : ; do
  # Check service status by detecting if the port is listening
  if curl -sSf "${KEYCLOAK_ADDR}" >/dev/null; then
    echo "keycloak has started successfully!"
    break
  fi

  # Timeout detection
  if [ $MAX_WAIT -ne 0 ]; then
    current_time=$(date +%s)
    if (( current_time - start_time > MAX_WAIT )); then
      echo "Error: keycloak startup not detected within ${MAX_WAIT} seconds"
      exit 1
    fi
  fi

  echo "Waiting for keycloak ${KEYCLOAK_ADDR} to start... (waited $(( $(date +%s) - start_time )) seconds)"
  sleep 5
done



python3 keycloak/keycloak-import.py      \
    --url "${KEYCLOAK_ADDR}"            \
    --username "admin"                  \
    --password "${PASSWORD_KEYCLOAK}"   \
    --fname "./keycloak/realm-export.json" \
    --client-name "${KEYCLOAK_USERNAME}"      \
    --client-password "${KEYCLOAK_PASSWORD}"
