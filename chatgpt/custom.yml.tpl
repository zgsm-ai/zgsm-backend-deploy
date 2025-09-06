app:
  PEDESTAL_SERVER:
    server_url: "{{AI_GATEWAY_ADDR}}"
    api_key: "{{CHAT_APIKEY}}"
celery:
  broker_url: "redis://redis:6379/0"
  result_backend: "redis://redis:6379/1"
