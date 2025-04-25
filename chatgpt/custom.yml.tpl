app:
  PEDESTAL_SERVER:
    server_url: "http://one-api:30000"
    api_key: "966c3157fe65461dbc731cd540b6cd5d"
celery:
  broker_url: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/0"
  result_backend: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/1"
