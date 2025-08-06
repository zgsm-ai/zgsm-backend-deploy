#!/bin/sh

. ./utils.sh
. ./configure.sh

DEPLOY="$(basename "$(dirname "$(readlink -f "$0")")")"

retry "docker compose -f docker-compose-initdb.yml up -d" 60 5 || fatal "Failed to start postgres"

sleep 5

# 遍历postgres/scripts目录下的.sql文件
for sql_file in postgres/scripts/*.sql; do
    # 短路返回：如果不是文件则跳过
    [ ! -f "$sql_file" ] && continue
    
    # 获取文件名（不包含路径）
    filename=$(basename "$sql_file")
    # 去掉.sql后缀得到数据库名前缀
    db=$(basename "$sql_file" .sql)
    echo "正在执行SQL文件: $filename，目标数据库: $db"
    
    # 执行SQL文件的命令，使用文件名前缀作为数据库名
    docker exec -i "${DEPLOY}-postgres-1" /usr/local/bin/psql -U $POSTGRES_USER -d $db -f "/scripts/$filename"
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
