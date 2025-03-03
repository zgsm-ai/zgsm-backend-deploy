app:
  PEDESTAL_SERVER:
    server_url: "https://api.deepseek.com"
    api_key: "sk-f97d231c3e4a4d7f959e79543c0c99dc"  
#    api_key: "sk-e0d345b888b6445faef8c583b454141d"
celery:
  broker_url: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/0"
  result_backend: "redis://{{ZGSM_BACKEND}}:{{PORT_REDIS}}/1"
