#!/bin/sh

docker compose --profile initdb up chatgpt-initdb
docker compose down
