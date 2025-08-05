#!/bin/sh

. ./utils.sh
. ./configure.sh

DEPLOY="$(basename "$(dirname "$(readlink -f "$0")")")"

retry "docker compose -f docker-compose-initdb.yml up -d" 60 5 || fatal "Failed to start postgres"

sleep 10

# 遍历postgres/scripts目录下的.sql文件
for sql_file in postgres/scripts/*.sql; do
    if [ -f "$sql_file" ]; then
        # 获取文件名（不包含路径）
        filename=$(basename "$sql_file")
        # 去掉.sql后缀得到数据库名前缀
        db_name=$(basename "$sql_file" .sql)
        echo "正在执行SQL文件: $filename，目标数据库: $db_name"
        
        # 执行SQL文件的命令，使用文件名前缀作为数据库名
        CMD='docker exec -it '"${DEPLOY}-postgres-1"' /usr/local/bin/psql -U '"$POSTGRES_USER"' -d '"$db_name"' -f "/scripts/'"$filename"'"'
        retry "$CMD" 60 5 || fatal "Failed to execute $filename in database $db_name"
    fi
done

SQL="SELECT datname AS database_name FROM pg_database ORDER BY datname;"
CMD='docker exec -it '"${DEPLOY}-postgres-1"' /usr/local/bin/psql -U '"$POSTGRES_USER"' -h 127.0.0.1 -p '"$PORT_POSTGRES"' -c "'"$SQL"'"'
retry "$CMD" 60 5 || fatal "Failed to create databases"

# 定义需要创建的数据库列表
DBLIST="chatgpt auth oneapi quota_manager codereview casdoor codebase_indexer"
for db in $DBLIST; do
    SQL="SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;"
    CMD='docker exec -it '"${DEPLOY}-postgres-1"' /usr/local/bin/psql -U '"$POSTGRES_USER"' -h 127.0.0.1 -p '"$PORT_POSTGRES"' -d '"$db"' -c "'"$SQL"'"'
    echo $CMD
    retry "$CMD" 60 5  || fatal "Failed to show $db database"
done

retry "docker compose -f docker-compose-initdb.yml down" 60 3 || fatal "Failed to stop postgres"

# retry "docker compose up chatgpt-initdb" 60 5 || fatal "Failed to initialize database"
