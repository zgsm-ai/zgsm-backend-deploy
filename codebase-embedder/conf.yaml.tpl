Name: codebase-embedder
Host: 0.0.0.0
Port: 8888
Timeout: 120000 #ms
MaxConns: 500
MaxBytes: 104857600 # 100MB
DevServer:
  Enabled: true
Verbose: false
Mode: test # dev,test,rt,pre, pro
  
Auth:
  UserInfoHeader: "x-userinfo"
Database:
  Driver: postgres
  DataSource: postgres://{{POSTGRES_USER}}:{{PASSWORD_POSTGRES}}@postgres:5432/codebase_embedder?sslmode=disable
  AutoMigrate:
    enable: true    
IndexTask:
  PoolSize: 1000
  QueueSize: 100
  LockTimeout: 10s
  EmbeddingTask:
    PoolSize: 20
    MaxConcurrency: 10
    Timeout: 18000s
    OverlapTokens: 100
    MaxTokensPerChunk: 1000
    EnableMarkdownParsing: false
    EnableOpenAPIParsing: false
  GraphTask:
    MaxConcurrency: 100
    Timeout: 18000s
    ConfFile: "etc/codegraph.yaml"

Cleaner:
  Cron: "0 0 * * *"
  CodebaseExpireDays: 30

Redis:
  Addr: redis:6379
  DefaultExpiration: 1h

VectorStore:
  Type: weaviate
  Timeout: 60s
  MaxRetries: 5
  StoreSourceCode: false
  FetchSourceCode: true
  BaseURL: http://codebase-querier:8888/codebase-indexer/api/v1/snippets/read
  Weaviate:
    MaxDocuments: 20
    Endpoint: "weaviate:8080"
    BatchSize: 100
    ClassName: "CodebaseIndex"
  Embedder:
    Timeout: 30s
    MaxRetries: 3
    BatchSize: 10
    StripNewLines: true
    Model: {{EMBEDDER_MODEL}}
    ApiKey: {{EMBEDDER_APIKEY}}
    ApiBase: {{EMBEDDER_BASEURL}}
  Reranker:
    Timeout: 10s
    MaxRetries: 3
    Model: {{RERANKER_MODEL}}
    ApiKey: {{RERANKER_APIKEY}}
    ApiBase: {{RERANKER_BASEURL}}

Log:
  Mode: console # console,file,volume
  ServiceName: "codebase-embedder"
  Encoding: plain # json,plain
  Path: "/app/logs"
  Level: info # debug,info,error,severe
  KeepDays: 7
  MaxSize: 100 # MB per file, take affect when Rotation is size.
  Rotation: daily # split by day or size
Validation:
  enabled: true
  check_content: true
  fail_on_mismatch: false
  log_level: "info"
  max_concurrency: 5
  skip_patterns: []
TokenLimit:
  max_running_tasks: 100  
  enabled: true 
HealthCheck:
  Enabled: true
  URL: http://codebase-querier:8888/codebase-indexer/api/v1/index/summary
  Timeout: 3s
