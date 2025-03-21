server:
  port: 9696
  servlet:
    context-path: /

spring:
  redis:
    host: {{ZGSM_BACKEND}}
    port: 6379
    password:  #Redis服务器连接密码（默认为空）
    timeout: 360000 #连接超时时间（毫秒）
    jedis:
      pool:
        max-active: 20 # 连接池最大连接数（使用负值表示没有限制）
        max-wait: -1 # 连接池最大阻塞等待时间（使用负值表示没有限制）
        max-idle: 10 # 连接池中的最大空闲连接
        min-idle: 0 # 连接池中的最小空闲连接
