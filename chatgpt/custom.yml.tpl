app:
  PEDESTAL_SERVER:
    server_url: "{{CHAT_AIGW_ADDR}}"
    api_key: "{{CHAT_API_KEY}}"
celery:
  broker_url: "redis://redis:{{PORT_REDIS}}/0"
  result_backend: "redis://redis:{{PORT_REDIS}}/1"
