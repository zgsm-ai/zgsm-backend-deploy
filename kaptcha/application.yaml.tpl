server:
  port: 9696
  servlet:
    context-path: /

spring:
  redis:
    host: {{ZGSM_BACKEND}}
    port: 6379
    password:  # Redis server connection password (default is empty)
    timeout: 360000 # Connection timeout (milliseconds)
    jedis:
      pool:
        max-active: 20 # Maximum number of connections in the connection pool (use a negative value to indicate no limit)
        max-wait: -1 # Maximum blocking wait time for the connection pool (use a negative value to indicate no limit)
        max-idle: 10 # Maximum idle connections in the connection pool
        min-idle: 0 # Minimum idle connections in the connection pool
