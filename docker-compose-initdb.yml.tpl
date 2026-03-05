services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      TZ: "Asia/Shanghai"
      POSTGRES_DB: "{{POSTGRES_DB}}"
      POSTGRES_USER: "{{POSTGRES_USER}}"
      POSTGRES_PASSWORD: "{{PASSWORD_POSTGRES}}"
    volumes:
      - ./postgres/data:/var/lib/postgresql/data
      - ./postgres/initdb.d:/docker-entrypoint-initdb.d
      - ./postgres/scripts:/scripts
    ports:
      - "{{PORT_POSTGRES}}:5432/tcp"
    networks:
      - shenma
    # 添加启动命令，配置PostgreSQL参数
    command: >
      postgres
      -c max_connections=200
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c default_statistics_target=100
      -c random_page_cost=1.1
      -c effective_io_concurrency=200
      -c work_mem=4MB
      -c checkpoint_timeout=10min
    # 添加容器资源限制
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

networks:
  shenma:
    driver: bridge

