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
  model: "{{CODEREVIEW_MODEL}}"
  stage_models:
    check: "{{CODEREVIEW_MODEL}}"
    review: "{{CODEREVIEW_MODEL}}"
    annotation: "{{CODEREVIEW_MODEL}}"
    title: "{{CODEREVIEW_MODEL}}"
context_types:
  allow_skip_context: true
http_client:
  services:
    chatRag:
      base_url: "http://chat-rag:8888/chat-rag/api/v1"
    kbCenter:
      base_url: "http://codebase-querier:8888/codebase-indexer/api/v1"