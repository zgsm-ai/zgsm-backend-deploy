version: '3.8'

services:
  apisix:
    image: {{IMAGE_APISIX}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./apisix/config.yaml:/usr/local/apisix/conf/config.yaml:ro
    depends_on:
      - etcd
    ports:
      - "{{PORT_APISIX_API}}:9180/tcp"
      - "{{PORT_APISIX_ENTRY}}:9080/tcp"
    #  - "{{PORT_APISIX_PROMETHEUS}}:9091/tcp"
    networks:
      - shenma

  etcd:
    image: {{IMAGE_ETCD}}
    restart: always
    volumes:
      - ./etcd/data:/bitnami/etcd/data
    user: "1000:1000"
    environment:
      TZ: "Asia/Shanghai"
      ETCD_ENABLE_V2: "true"
      ALLOW_NONE_AUTHENTICATION: "yes"
      ETCD_ADVERTISE_CLIENT_URLS: "http://127.0.0.1:2379"
      ETCD_LISTEN_CLIENT_URLS: "http://0.0.0.0:2379"
    ports:
      - "{{PORT_ETCD}}:2379/tcp"
    networks:
      - shenma

  redis:
    image: {{IMAGE_REDIS}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis/data:/data
    ports:
      - "{{PORT_REDIS}}:6379"
    networks:
      - shenma

  postgres:
    image: {{IMAGE_POSTGRES}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
      POSTGRES_DB: "{{POSTGRES_DB}}"
      POSTGRES_USER: "{{POSTGRES_USER}}"
      POSTGRES_PASSWORD: "{{PASSWORD_POSTGRES}}"
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
    ports:
      - "{{PORT_POSTGRES}}:5432/tcp"
    networks:
      - shenma
  mysql:
    image: {{IMAGE_MYSQL}}
    container_name: mysql
    restart: unless-stopped
    
    # 从环境变量读取配置
    environment:
      MYSQL_ROOT_PASSWORD: costrict-root
      MYSQL_DATABASE: mysql
      MYSQL_USER: nacos
      MYSQL_PASSWORD: nacos
    command: >
      --sort_buffer_size=4194304
      --read_rnd_buffer_size=8388608
      --join_buffer_size=4194304
      --tmp_table_size=67108864
      --max_heap_table_size=67108864
    ports:
      - "33306:3306"
    
    volumes:
      # 持久化数据
      - ./mysql/data:/var/lib/mysql
      # 初始化脚本（首次启动时执行）
      - ./mysql/init-scripts:/docker-entrypoint-initdb.d
    networks:
      - shenma
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  nacos:
    image: {{IMAGE_NACOS}}
    container_name: nacos
    environment:
      # 必选：使用外置 MySQL 模式
      - MODE=standalone
      - SPRING_DATASOURCE_PLATFORM=mysql
      - MYSQL_SERVICE_HOST=mysql
      - MYSQL_SERVICE_PORT=3306
      - MYSQL_SERVICE_DB_NAME=nacos
      - MYSQL_SERVICE_USER=nacos
      - MYSQL_SERVICE_PASSWORD=nacos
      - MYSQL_SERVICE_DB_PARAM=characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&allowPublicKeyRetrieval=true
      # 可选：JVM 内存配置（根据服务器资源调整）
      - JVM_XMS=512m
      - JVM_XMX=512m
      - JVM_XMN=256m
      - NACOS_AUTH_IDENTITY_KEY=nacos
      - NACOS_AUTH_IDENTITY_VALUE=nacos
      - NACOS_AUTH_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTI=
    ports:
    #   - "31848:8848"   # Nacos 主端口
      - "31808:8080"   # 管理端口
    #   - "9848:9848"   # gRPC 端口（Nacos 2.x+ 需要）
    #   - "9849:9849"   # gRPC 端口（Nacos 2.x+ 需要）
    restart: unless-stopped
    depends_on:
      - mysql
    networks:
      - shenma
  weaviate:
    image: {{IMAGE_WEAVIATE}}
    restart: always
    ports:
      - "{{PORT_WEAVIATE}}:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
      PERSISTENCE_DATA_PATH: "/var/lib/weaviate"
      DEFAULT_VECTORIZER_MODULE: "none"
      ENABLE_MODULES: ""
      CLUSTER_HOSTNAME: "weaviate"
      ASYNC_INDEXING: "true"
      AUTHENTICATION_APIKEY_ENABLED: "false"
    volumes:
      - ./weaviate/data:/var/lib/weaviate
    networks:
      - shenma

  portal:
    image: {{IMAGE_NGINX}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./portal/data:/var/www
      - ./portal/nginx.conf:/etc/nginx/nginx.conf
    #ports:
    #  - "{{PORT_PORTAL}}:80/tcp"
    networks:
      - shenma

  chat-rag:
    image: {{IMAGE_CHATRAG}}
    command: ["/app/chat-rag", "-f", "/app/etc/chat-api.yaml"]
    restart: always
    #ports:
    #  - ":8888"
    volumes:
      - ./chat-rag/logs:/data/logs
      - ./chat-rag/chat-api.yaml:/app/etc/chat-api.yaml:ro
      - ./chat-rag/rules.yaml:/app/etc/rules.yaml:ro
    depends_on:
      - redis
      - higress
      - nacos
    networks:
      - shenma

  review-manager:
    image: {{IMAGE_REVIEW_MANAGER}}
    container_name: review-manager
    # ports:
    #   - "8080:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./codereview/config/review-manager-config.yaml:/app/config/config.local.yaml:ro
      - ./codereview/workspaces_data:/home/appuser/Workspaces
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    networks:
      - shenma

  # Review Worker
  review-worker:
    image: {{IMAGE_REVIEW_MANAGER}}
    container_name: review-worker
    command: ["/bin/sh", "-c", "./review-manager worker"]
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./codereview/config/review-manager-config.yaml:/app/config/config.local.yaml:ro
      - ./codereview/workspaces_data:/home/appuser/Workspaces
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    networks:
      - shenma

  # Issue Manager
  issue-manager:
    image: {{IMAGE_ISSUE_MANAGER}}
    container_name: issue-manager
    ports:
      - "8081:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./codereview/config/issue-manager-config.yaml:/app/config/config.local.yaml:ro
    depends_on:
      - postgres
    networks:
      - shenma

  # Review Checker
  review-checker:
    image: {{IMAGE_REVIEW_CHECKER}}
    # container_name 在使用 --scale 时会冲突，已注释
    # container_name: review-checker
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./codereview/config/review-checker-config.yaml:/app/config/config.local.yaml:ro
      - ./codereview/config/base/config/costrict/costrict.json:/app/base/.config/costrict/costrict.json:ro
      - ./codereview/config/base/cclsp.json:/app/base/cclsp.json:ro
      - ./codereview/config/base/prompts/CodeReviewerPrompt.md:/app/base/prompts/CodeReviewerPrompt.md:ro
      - ./codereview/config/base/prompts/ReflectionAgentPrompt.md:/app/base/prompts/ReflectionAgentPrompt.md:ro
      - ./codereview/workspaces_data:/home/appuser/Workspaces
    depends_on:
      - issue-manager
      - postgres
      - redis
    networks:
      - shenma

  credit-manager:
    image: {{IMAGE_CREDIT_MANAGER}}
    command: ["nginx", "-g", "daemon off;"]
    restart: always
    #ports:
    #  - "{{PORT_CREDIT_MANAGER}}:80"
    volumes:
      - ./credit-manager/config:/config
    networks:
      - shenma

  oidc-auth:
    image: {{IMAGE_OIDC_AUTH}}
    restart: always
    #ports:
    #  - "{{PORT_OIDC_AUTH}}:8080"
    depends_on:
      - postgres
    environment:
      SERVER_BASEURL: "{{COSTRICT_BACKEND_BASEURL}}"
      PROVIDERS_CASDOOR_CLIENTID: {{OIDC_AUTH_CLIENT_ID}}
      PROVIDERS_CASDOOR_CLIENTSECRET: "{{OIDC_AUTH_CLIENT_SECRET}}"
      PROVIDERS_CASDOOR_BASEURL: "{{COSTRICT_BACKEND_BASEURL}}"
      PROVIDERS_CASDOOR_INTERNALURL: "{{OIDC_CASDOOR_ADDR}}"
      SMS_ENABLEDTEST: true
      SMS_CLIENTID: 
      SMS_CLIENTSECRET: 
      SMS_TOKENURL: 
      SMS_SENDURL: 
      SYNCSTAR_ENABLED: false
      SYNCSTAR_PERSONALTOKEN: 
      SYNCSTAR_OWNER: zgsm-ai
      SYNCSTAR_REPO: zgsm
      DATABASE_HOST: postgres
      DATABASE_DBNAME: auth
      DATABASE_PASSWORD: {{PASSWORD_POSTGRES}}
      DATABASE_PORT: 5432
      DATABASE_USERNAME: {{POSTGRES_USER}}
      ENCRYPT_AESKEY: pUD8mylndVVK7hTNt56VZMkNrppinbNg
    volumes:
      - ./oidc-auth/logs:/app/logs
    networks:
      - shenma

  code-completion:
    image: {{IMAGE_CODE_COMPLETION}}
    restart: always
    #ports:
    #  - "{{PORT_COMPLETION}}:5000/tcp"
    environment:
      TZ: Asia/Shanghai
    depends_on:
      - codebase-querier
    networks:
      - shenma

  codebase-querier:
    image: {{IMAGE_CODEBASE_QUERIER}}
    restart: always
    command: ["/app/server", "-f", "/app/conf/conf.yaml"]
    #ports:
    #  - "{{PORT_CODEBASE_QUERIER}}:8888"
    depends_on:
      - cotun
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./codebase-querier/conf.yaml:/app/conf/conf.yaml:ro
      - ./codebase-querier/logs:/app/logs
    networks:
      - shenma
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8888/health"]
      interval: 20s
      timeout: 5s
      retries: 3
      start_period: 15s

  codebase-embedder:
    image: {{IMAGE_CODEBASE_EMBEDDER}}
    restart: always
    command: ["/app/server", "-f", "/app/conf/conf.yaml"]
    #ports:
    #  - "{{PORT_CODEBASE_EMBEDDER}}:8888"
    environment:
      - TZ=Asia/Shanghai
      - INDEX_NODE=1
    volumes:
      - ./codebase-embedder/conf.yaml:/app/conf/conf.yaml:ro
      - ./codebase-embedder/logs:/app/logs
    networks:
      - shenma
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8888/health"]
      interval: 20s
      timeout: 5s
      retries: 3
      start_period: 15s
    depends_on:
      - codebase-querier
      - postgres
      - redis
      - weaviate

  cotun:
    image: {{IMAGE_COTUN}}
    restart: always
    command: ["--reverse", "--port", "8080", "--authfile", "/cotun/users.json"]
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./cotun/users.json:/cotun/users.json
    #ports:
    #  - "{{PORT_COTUN}}:8080/tcp"
    #  - "{{PORT_COTUN2}}:7890/tcp"
    networks:
      - shenma

  casdoor:
    image: {{IMAGE_CASDOOR}}
    restart: always
    ports:
      - "{{PORT_CASDOOR}}:8000"
    environment:
      driverName: postgres
      dataSourceName: "host=postgres port=5432 user={{POSTGRES_USER}} password={{PASSWORD_POSTGRES}} dbname=casdoor sslmode=disable"
    depends_on:
      - postgres
    networks:
      - shenma

  higress:
    image: {{IMAGE_HIGRESS}}
    restart: always
    ports:
    #  - "{{PORT_AI_GATEWAY}}:8080"
      - "{{PORT_HIGRESS_CONTROL}}:8001"
    environment:
      MODE: full
      O11Y: on
      CONFIG_TEMPLATE: ai-gateway
      GATEWAY_HTTP_PORT: 8080
      GATEWAY_HTTPS_PORT: 8443
      CONSOLE_PORT: 8001
    volumes:
      - ./higress/data:/data
    depends_on:
      - portal
    networks:
      - shenma

  prometheus:
    image: {{IMAGE_PROMETHEUS}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "{{PORT_PROMETHEUS}}:9090"
    depends_on:
      - apisix
    networks:
      - shenma

  grafana:
    image: {{IMAGE_GRAFANA}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    ports:
      - "{{PORT_GRAFANA}}:3000"
    volumes:
      - "./grafana/provisioning:/etc/grafana/provisioning"
      - "./grafana/dashboards:/var/lib/grafana/dashboards"
      - "./grafana/config/grafana.ini:/etc/grafana/grafana.ini"
    depends_on:
      - prometheus
      - es
    networks:
      - shenma

  es:
    image: {{IMAGE_ES}}
    environment:
      TZ: Asia/Shanghai
      discovery.type: single-node
      bootstrap.memory_lock: true
      xpack.security.enabled: false
      xpack.security.http.ssl.enabled: false  # Disable HTTPS
      xpack.ml.enabled: false
      ELASTIC_PASSWORD: "{{PASSWORD_ELASTIC}}"
      ES_JAVA_OPTS: "-Xms512m -Xmx512m"
    user: "1000:1000"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "{{PORT_ES}}:9200"
    volumes:
      - ./es/data:/usr/share/elasticsearch/data
    networks:
      - shenma

networks:
  shenma:
    driver: bridge

