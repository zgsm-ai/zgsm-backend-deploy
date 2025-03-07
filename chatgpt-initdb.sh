#!/bin/sh

docker compose up postgres -d
sleep 5
docker exec -it zgsm-compose-deploy-postgres-1 /usr/local/bin/psql -U keycloak -h127.0.0.1 -p5432 -c "CREATE DATABASE chatgpt;"
docker compose --profile initdb up chatgpt-initdb
sleep 5
docker compose down
