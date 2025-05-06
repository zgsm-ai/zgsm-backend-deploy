#!/bin/sh

. ./utils.sh

retry "docker compose up postgres -d" 60 5 || fatal "Failed to start postgres"
# ERROR: database "chatgpt" already exists indicates the database is already created, no retry
create_chatgpt_db_cmd='docker exec -it zgsm-backend-deploy-postgres-1 /usr/local/bin/psql -U keycloak -h127.0.0.1 -p5432 -c "CREATE DATABASE chatgpt;"'
retry "$create_db_cmd" 60 5 "already exists" || fatal "Failed to create chatgpt database"
create_oneapi_db_cmd='docker exec -it zgsm-backend-deploy-postgres-1 /usr/local/bin/psql -U keycloak -h127.0.0.1 -p5432 -c "CREATE DATABASE oneapi;"'
retry "$create_oneapi_db_cmd" 60 5 "already exists" || fatal "Failed to create oneapi database"  # Note: Original Chinese contains "chatgpt" error
retry "docker compose up chatgpt-initdb" 60 5 || fatal "Failed to initialize database"
