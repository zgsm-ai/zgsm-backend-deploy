Name: codebase-indexer
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
  DataSource: postgres://{{POSTGRES_USER}}:{{PASSWORD_POSTGRES}}@postgres:{{PORT_POSTGRES}}/codebase_indexer?sslmode=disable
  AutoMigrate:
    enable: true    
IndexTask:
  PoolSize: 50
  QueueSize: 100
  LockTimeout: 610s
  Topic: "codebase_indexer:mq:sync"
  EmbeddingTask:
    PoolSize: 10
    MaxConcurrency: 10
    Timeout: 600s
    OverlapTokens: 100
    MaxTokensPerChunk: 1000
  GraphTask:
    PoolSize: 10
    MaxConcurrency: 10
    Timeout: 600s
    ConfFile: "/app/conf/codegraph.yaml"
    
Cleaner:
  Cron: "0 0 * * *"
  CodebaseExpireDays: 3
    
Redis:
  Addr: redis:{{PORT_REDIS}}
    
MessageQueue:
  Type: redis
    
CodeBaseStore:
  local:
    BasePath: /mnt/codebase-store
    
VectorStore:
  Type: weaviate
  Timeout: 60s
  MaxRetries: 5
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
    Model: gte-modernbert-base
    ApiKey: "aee59212-46c5-4726-807a-cb9121c2ab5f&code=5650566a-626c-4fcb-a490-f3f3099b7105.aee59212-46c5-4726-807a-cb9121c2ab5f.6aa578f3-e98d-40b7-bbdd-c344bc4861e0"
    ApiBase: https://zgsm.sangfor.com/v1/
  Reranker:
    Timeout: 10s
    MaxRetries: 3
    Model: gte-reranker-modernbert-base
    ApiKey: "123"
    ApiBase: https://zgsm.sangfor.com/v1/rerank
    
Log:
  Mode: volume # console,file,volume
  ServiceName: "codebase-indexer"
  Encoding: plain # json,plain
  Path: "/app/logs"
  Level: info # debug,info,error,severe
  KeepDays: 7
  MaxSize: 100 # MB per file, take affect when Rotation is size.
  Rotation: daily # split by day or size