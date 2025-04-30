# Basic settings for running in production. Change accordingly before deploying the server.
# Database
# The database vendor.
db=postgres
# The username of the database user.
db-username=keycloak
# The password of the database user.
db-password={{PASSWORD_POSTGRES}}
# The full database JDBC URL. If not provided, a default URL is set based on the selected database vendor.
db-url=jdbc:postgresql://postgres/keycloak

# Observability
# If the server should expose healthcheck endpoints.
#health-enabled=true
# If the server should expose metrics endpoints.
#metrics-enabled=true

# HTTP
# The file path to a server certificate or certificate chain in PEM format.
#https-certificate-file=${kc.home.dir}conf/server.crt.pem
# The file path to a private key in PEM format.
#https-certificate-key-file=${kc.home.dir}conf/server.key.pem
# The proxy address forwarding mode if the server is behind a reverse proxy.
#proxy=reencrypt
# Do not attach route to cookies and rely on the session affinity capabilities from reverse proxy
#spi-sticky-session-encoder-infinispan-should-attach-route=false
# Hostname for the Keycloak server.
#hostname=myhostname

# 短信发送服务商
spi-phone-provider-config-sender-service=ntc
# 验证码有效期
spi-phone-provider-config-token-expires=300
# 默认区号
spi-phone-provider-config-default-areacode=86
# 区号配置信息
spi-phone-provider-config-areacode-config=${kc.home.dir:}/conf/areacode.json
# 锁定区号
spi-phone-provider-config-area-locked=true
# Which sms provider
spi-phone-default-service=ntc
# sms expires,default 60 second
spi-phone-default-token-expires-in=300
# How many send from ip address sms count in one hour, Zero is no limit. default 10
spi-phone-default-source-hour-maximum=50
# How many send to phone number sms count in one hour, Zero is no limit, default 3
spi-phone-default-target-hour-maximum=10
# allow one phone register multi user, default: false
spi-phone-default-gw-duplicate-phone=false
#Notice: will match after canonicalize number. eg: INTERNATIONAL: +41 44 668 18 00 , NATIONAL: 044 668 18 00 , E164: +41446681800
spi-phone-default-gw-default-number-regex=^\+?\d+$
# valid phone number, default: true
spi-phone-default-gw-valid-phone=false
#whether to parse user-supplied phone numbers and put into canonical International E.163 format.  _Required for proper duplicate phone number detection_
#[E164,INTERNATIONAL,NATIONAL,RFC3966], default: "" un-canonicalize;
spi-phone-default-gw-canonicalize-phone-numbers=E164
#a default region to be used when parsing user-supplied phone numbers. Lookup codes at https://www.unicode.org/cldr/cldr-aux/charts/30/supplemental/territory_information.html
#default: use realm setting's default Locate;
spi-phone-default-gw-phone-default-region=CN
#if compatible is true then search user will be use all format phone number
#default: false
spi-phone-default-gw-compatible=true
#Prevent 2FA from always happening for a period of time
#default: 60 * 60; 1 hour
spi-phone-default-gw-otp-expires=3600
# NTC发送的认证码信息模版
spi-phone-default-gw-message-template=[[code]],此认证码由诸葛神码发送，请勿泄露
# redis服务器IP
spi-captcha-service-default-redis-host=redis
# redis服务器端口
spi-captcha-service-default-redis-port={{PORT_REDIS}}
