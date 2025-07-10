database:
  type: postgres
  host: postgres
  port: {{PORT_POSTGRES}}
  user: {{POSTGRES_USER}}
  password: {{PASSWORD_POSTGRES}}
  dbname: codereview
redis:
  host: redis
  port: {{PORT_REDIS}}
  db: 0
kbcenter:
  skip_repository_check: true 
http_client:
  services:
    issueManager:
      base_url: "http://issue-manager:{{PORT_ISSUE_MANAGER}}/issue-manager/api/v1"
    kbCenter:
      base_url: "http://codebase-indexer:{{PORT_CODEBASE_INDEXER}}/codebase-indexer/api/v1"