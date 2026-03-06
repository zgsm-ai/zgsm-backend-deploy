database:
  type: postgres
  host: postgres
  port: 5432
  user: {{POSTGRES_USER}}
  password: {{PASSWORD_POSTGRES}}
  dbname: codereview
  pool:
    max_idle_conns: 3
    max_open_conns: 5
    conn_max_lifetime: 500
    conn_max_idle_time: 300
redis:
  host: redis
  port: 6379
  db: 0
git_repo:
  gitlab_token: ""
merge_request:
  max_diff_lines: 1000000
  max_file_count: 50
http_client:
  max_retries: 0
  services:
    issueManager:
      base_url: "http://issue-manager:8080/issue-manager/api/v1"
