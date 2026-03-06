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
  db: 2
http_client:
  services:
    issue_manager:
      base_url: "http://issue-manager:8080/issue-manager"
      max_retries: 3
