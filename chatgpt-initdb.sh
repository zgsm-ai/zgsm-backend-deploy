#!/bin/sh

docker compose --profile initdb up chatgpt-initdb
sleep 5
docker compose down
