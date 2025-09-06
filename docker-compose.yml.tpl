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
      - "{{PORT_APISIX_PROMETHEUS}}:9091/tcp"
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
      ETCD_ADVERTISE_CLIENT_URLS: "http://127.0.0.1:{{PORT_ETCD}}"
      ETCD_LISTEN_CLIENT_URLS: "http://0.0.0.0:{{PORT_ETCD}}"
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
    ports:
      - "{{PORT_PORTAL}}:80/tcp"
    networks:
      - shenma

  chat-rag:
    image: {{IMAGE_CHATRAG}}
    command: ["/app/chat-rag", "-f", "/app/etc/chat-api.yaml"]
    restart: always
    ports:
      - "{{PORT_CHAT_RAG}}:8888"
    volumes:
      - ./chat-rag/logs:/data/logs
      - ./chat-rag/chat-api.yaml:/app/etc/chat-api.yaml:ro
    depends_on:
      - codebase-querier
    networks:
      - shenma

  review-manager:
    image: {{IMAGE_REVIEW_MANAGER}}
    restart: always
    ports:
      - "{{PORT_REVIEW_MANAGER}}:8080"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: {{POSTGRES_USER}}
      DATABASE_PASSWORD: {{PASSWORD_POSTGRES}}
      DATABASE_NAME: codereview
      REDIS_HOST: redis
      REDIS_PORT: 6379
    volumes:
      - ./codereview/logs/review-manager:/app/logs
      - ./codereview/config/review-manager:/app/config
    networks:
      - shenma

  review-worker:
    image: {{IMAGE_REVIEW_MANAGER}}
    command: ./review-manager worker
    restart: always
    depends_on:
      - postgres
      - redis
      - review-manager
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: {{POSTGRES_USER}}
      DATABASE_PASSWORD: {{PASSWORD_POSTGRES}}
      DATABASE_NAME: codereview
      REDIS_HOST: redis
      REDIS_PORT: 6379
    volumes:
      - ./codereview/logs/review-worker:/app/logs
      - ./codereview/config/review-manager:/app/config
    networks:
      - shenma

  issue-manager:
    image: {{IMAGE_ISSUE_MANAGER}}
    restart: always
    ports:
      - "{{PORT_ISSUE_MANAGER}}:8080"
    depends_on:
      - postgres
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: {{POSTGRES_USER}}
      DATABASE_PASSWORD: {{PASSWORD_POSTGRES}}
      DATABASE_NAME: codereview
    volumes:
      - ./codereview/logs/issue-manager:/app/logs
      - ./codereview/config/issue-manager:/app/config
    networks:
      - shenma

  review-checker:
    image: {{IMAGE_REVIEW_CHECKER}}
    restart: always
    ports:
      - "{{PORT_REVIEW_CHECKER}}:8080"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_USER: {{POSTGRES_USER}}
      DATABASE_PASSWORD: {{PASSWORD_POSTGRES}}
      DATABASE_NAME: codereview
      REDIS_HOST: redis
      REDIS_PORT: 6379
      REDIS_DB: 2
    volumes:
      - ./codereview/logs/review-checker:/app/logs
      - ./codereview/config/review-checker:/app/config
    networks:
      - shenma

  credit-manager:
    image: {{IMAGE_CREDIT_MANAGER}}
    command: ["nginx", "-g", "daemon off;"]
    restart: always
    ports:
      - "{{PORT_CREDIT_MANAGER}}:80"
    volumes:
      - ./credit-manager/config:/config
    networks:
      - shenma

  oidc-auth:
    image: {{IMAGE_OIDC_AUTH}}
    restart: always
    ports:
      - "{{PORT_OIDC_AUTH}}:8080"
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

  quota-manager:
    image: {{IMAGE_QUOTA_MANAGER}}
    command: ["/app/quota-manager", "-c", "/app/app-conf.yml"]
    restart: always
    ports:
      - "{{PORT_QUOTA_MANAGER}}:8080"
    environment:
      TZ: Asia/Shanghai
      INDEX_NODE: "0"
    volumes:
      - ./quota-manager/app-conf.yml:/app/app-conf.yml
      - ./quota-manager/logs:/app/logs
    networks:
      - shenma

  chatgpt:
    image: {{IMAGE_CHAT_SERVER}}
    command: ["/sbin/entrypoint.sh", "app:start"]
    restart: always
    volumes:
      - ./chatgpt/server:/server
      - ./chatgpt/supervisor:/var/log/supervisor
      - ./chatgpt/logs:/server/logs
      - ./chatgpt/custom.yml:/custom.yml
    ports:
      - "{{PORT_CHATGPT_API}}:5000/tcp"
      - "{{PORT_CHATGPT_WS}}:8765/tcp"
      - "5555:5555/tcp"
    environment:
      - TZ=Asia/Shanghai
      - CACHE_DB=chatgpt
      - REDIS_URL=redis://redis:6379/0
      - SERVE_THREADS=200
      - SERVE_CONNECTION_LIMIT=512
      - PG_URL=postgres:5432
      - DB_NAME=chatgpt
      - DATABASE_URI=postgresext+pool://{{POSTGRES_USER}}:{{PASSWORD_POSTGRES}}@postgres/chatgpt
      - ES_SERVER=http://es:9200
      - ES_PASSWORD={{PASSWORD_ELASTIC}}
      - CUSTOM_CONFIG_FILE=/custom.yml
      - DEFAULT_MODEL_NAME={{CHAT_DEFAULT_MODEL}}
      - GEVENT_SUPPORT=True
      - NO_COLOR=1
      - DEPLOYMENT_TYPE=all
    depends_on:
      - redis
      - postgres
      - es
    networks:
      - shenma

  code-completion:
    image: {{IMAGE_CODE_COMPLETION}}
    restart: always
    ports:
      - "{{PORT_COMPLETION}}:5000/tcp"
    environment:
      - TZ=Asia/Shanghai
      - THRESHOLD_SCORE=0.3
      - STR_PATTERN=import +.*|from +.*|from +.* import *.*
      - USER_CODE_UPLOAD_DELAY=30
      - CONTEXT_LINES_LIMIT=1000
      - SNIPPET_TOP_N=0
      - MAX_TOKENS=500
      - MAX_MODEL_LEN=5000,1000
      - CODEBASE_INDEXER_API_BASE_URL=http://codebase-querier:8888
      - CONTEXT_COST_TIME=1500
      - MAX_MODEL_COST_TIME=2800
      - MAX_COST_TIME=3000
      - MULTI_LINE_STREAM_K=8
      - MIN_PREFIX_TOKEN=2000
      - COMPLETION_CACHE_TIME=86400
      - CONTINUE_COMPLETION_CACHE_EXPIRED=30
      - DISABLED_REJECT_AUTHORIZATION=True
      - ENABLE_REDIS=False
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_DB=0
      - REDIS_PWD="{{PASSWORD_REDIS}}"
      - MAIN_MODEL_TYPE=openai
      - OPENAI_MODEL_HOST={{COMPLETION_BASEURL}}
      - OPENAI_MODEL={{COMPLETION_MODEL}}
      - OPENAI_MODEL_API_KEY={{COMPLETION_APIKEY}}
      - OPENAI_MODEL_AUTHORIZATION=sk-CsPvPQwVPGVcPEBm6485D534F690407aA3113f7c13D633Cd
    depends_on:
      - redis
    networks:
      - shenma

  codebase-querier:
    image: {{IMAGE_CODEBASE_QUERIER}}
    restart: always
    command: ["/app/server", "-f", "/app/conf/conf.yaml"]
    ports:
      - "8888:8888"
      - "6060:6060"
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
    ports:
      - "8889:8888"
      - "6061:6060"
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

  cotun:
    image: {{IMAGE_COTUN}}
    restart: always
    command: ["server", "--reverse", "--port", "8080", "--authfile", "/cotun/users.json"]
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./cotun/users.json:/cotun/users.json
    ports:
      - "{{PORT_COTUN}}:8080/tcp"
    networks:
      - shenma

  tunnel-manager:
    image: {{IMAGE_TUNNEL_MANAGER}}
    restart: always
    environment:
      TZ: "Asia/Shanghai"
    ports:
      - "{{PORT_TUNNEL_MANAGER}}:8080"
    volumes:
      - ./tunnel-manager/config.yaml:/config.yaml
      - ./tunnel-manager/data:/data
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
      - "{{PORT_AI_GATEWAY}}:8080"
      - "{{PORT_HIGRESS_CONTROL}}:8001"
    environment:
      - "MODE=full"
      - "O11Y=on"
      - "CONFIG_TEMPLATE=ai-gateway"
      - "GATEWAY_HTTP_PORT=8080"
      - "GATEWAY_HTTPS_PORT=8443"
      - "CONSOLE_PORT=8001"
    volumes:
      - ./higress/data:/data
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
      - TZ=Asia/Shanghai
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
      - xpack.security.http.ssl.enabled=false  # Disable HTTPS
      - xpack.ml.enabled=false
      - "ELASTIC_PASSWORD={{PASSWORD_ELASTIC}}"
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    user: "1000:1000"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "{{PORT_ES}}:9200"
      - "9300:9300"
    volumes:
      - ./es/data:/usr/share/elasticsearch/data
    networks:
      - shenma

networks:
  shenma:
    driver: bridge

