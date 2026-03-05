database:
  type: postgres
  host: postgres
  port: 5432
  user: {{POSTGRES_USER}}
  password: {{PASSWORD_POSTGRES}}
  dbname: codereview
redis:
  host: redis
  port: 6379
  db: 2
chat_rag:
  model: "{{CHAT_DEFAULT_MODEL}}"
context_types:
  allow_skip_context: true
check_config:
  enabled_template_tags:
    - tag: "通用专家"
    - tag: "内存专家"
    - tag: "通用评审"
    - tag: "标题生成"
http_client:
  services:
    chatRag:
      base_url: "http://chat-rag:8888/chat-rag/api/v1"
    kbCenter:
      base_url: "http://codebase-querier:8888/codebase-indexer/api/v1"