database:
  type: postgres
  host: postgres
  port: {{PORT_POSTGRES}}
  user: {{POSTGRES_USER}}
  password: {{PASSWORD_POSTGRES}}
  dbname: codereview
redis:
  host: redis
  port: {{PORT_REDIS}}
  db: 2
chat_rag:
  model: "deepseek-v3"
context_types:
  allow_skip_context: true
http_client:
  services:
    chatRag:
      base_url: "http://chat-rag:{{PORT_CHAT_RAG}}/chat-rag/api/v1"
    kbCenter:
      base_url: "http://codebase-indexer:{{PORT_CODEBASE_INDEXER}}/codebase-indexer/api/v1"