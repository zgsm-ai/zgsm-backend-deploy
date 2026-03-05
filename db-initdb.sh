#!/bin/sh

. ./utils.sh
. ./configure.sh

DEPLOY="$(basename "$(dirname "$(readlink -f "$0")")")"

retry "docker compose -f docker-compose-initdb.yml up -d" 60 5 || fatal "Failed to start postgres"

sleep 5

# 等待PostgreSQL完全启动
echo "等待PostgreSQL完全启动..."
for i in {1..30}; do
    if docker exec "${DEPLOY}-postgres-1" pg_isready -U $POSTGRES_USER -q; then
        echo "PostgreSQL已准备就绪"
        break
    else
        echo "等待PostgreSQL启动... ($i/30)"
        sleep 2
    fi
done


SQL="SELECT datname AS database_name FROM pg_database ORDER BY datname;"
docker exec -i "${DEPLOY}-postgres-1" /usr/local/bin/psql -U $POSTGRES_USER -c "$SQL"

# 定义需要创建的数据库列表
DBLIST="chatgpt auth oneapi quota_manager codereview casdoor codebase_indexer"
for db in $DBLIST; do
    SQL="SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
    echo "--------------------------------------------------------------------------"
    echo "db: ${db}"
    echo "$SQL"
    echo "--------------------------------------------------------------------------"
    docker exec -i "${DEPLOY}-postgres-1" /usr/local/bin/psql -U $POSTGRES_USER -d $db -c "$SQL"
done

retry "docker compose -f docker-compose-initdb.yml down" 60 3 || fatal "Failed to stop postgres"
