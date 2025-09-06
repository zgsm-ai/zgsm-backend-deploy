database:
  host: "postgres"
  port: 5432
  user: "{{POSTGRES_USER}}"
  password: "{{PASSWORD_POSTGRES}}"
  dbname: "quota_manager"
  sslmode: "disable"

auth_database:
  host: "postgres"
  port: 5432
  user: "{{POSTGRES_USER}}"
  password: "{{PASSWORD_POSTGRES}}"
  dbname: "auth"
  sslmode: "disable"

aigateway:
  host: "higress"
  port: 8080
  admin_path: "/v1/chat/completions/quota"
  auth_header: "x-admin-key"
  auth_value: "12345678"

server:
  port: 8080
  mode: "release"
  token_header: "authorization"

scheduler:
  scan_interval: "0 * * * * *" # Scan every hour

voucher:
  signing_key: "e8a3b2d1c0f9e7d6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2"

github_star_check:
  enabled: false
  required_repo: "zgsm-ai.costrict"

log:
  level: "warn"
  stdout_only: true