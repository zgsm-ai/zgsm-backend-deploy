issuer: http://dex:5556/dex
storage:
  type: postgres
  config:
    host: postgres
    port: 5432
    database: dex
    user: keycloak
    password: {{PASSWORD_POSTGRES}}
    ssl:
      mode: disable
web:
  http: 0.0.0.0:5556
logger:
  level: "debug"
  format: text
oauth2:
  skipApprovalScreen: true
enablePasswordDB: false
staticClients:
  - id: "1449280978"
    redirectURIs:
      - http://apisix:{{PORT_APISIX_ENTRY}}/login/ok
    name: 'Dex Login Application'
    secret: "49a2e85e8fbe81ce5bf768889c8e2a9b"
    grantTypes:
      - "authorization_code"
      - "refresh_token"
    responseTypes:
      - "code"
    scopes:
      - "openid"
      - "profile"
      - "email"
      - "federated:id"
# connectors:
#   - type: oauth
#     id: idtrust
#     name: IDtrust
#     config:
#       clientID: "1449280978"
#       clientSecret: "49a2e85e8fbe81ce5bf768889c8e2a9b"
#       redirectURI: http://dex:5556/dex/callback
#       tokenURL: {{redirect_url}}
#       authorizationURL: {{authorizationURL}}
#       userInfoURL: {{userInfoURL}}
#       logoutURL: {{logoutURL}}
#       userIDKey: employee_number
#       claimMapping:
#         userNameKey: username
routes:
  - path: /dex/auth/idtrust
    connectorID: idtrust