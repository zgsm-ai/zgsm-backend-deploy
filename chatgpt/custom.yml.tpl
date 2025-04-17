app:
  PEDESTAL_SERVER:
    server_url: "http://{{ONE_API_HOST}}:{{ONE_API_PORT}}"
    api_key: "{{ONE_API_INITIAL_ROOT_ACCESS_TOKEN}}"
celery:
  broker_url: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/0"
  result_backend: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/1"
