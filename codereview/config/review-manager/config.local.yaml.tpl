database:
  type: postgres
  host: postgres
  port: 5432
  user: {{POSTGRES_USER}}
  password: {{PASSWORD_POSTGRES}}
  dbname: codereview
redis:
  host: redis
  port: 6379
  db: 0
kbcenter:
  skip_repository_check: false 
http_client:
  services:
    issueManager:
      base_url: "http://issue-manager:8080/issue-manager/api/v1"
    kbCenter:
      base_url: "http://codebase-querier:8888/codebase-indexer/api/v1"