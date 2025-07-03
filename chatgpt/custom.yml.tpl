app:
  PEDESTAL_SERVER:
    server_url: "http://172.31.86.242:8002"
    api_key: "966c3157fe65461dbc731cd540b6cd5d"
celery:
  broker_url: "redis://redis:{{PORT_REDIS}}/0"
  result_backend: "redis://redis:{{PORT_REDIS}}/1"
