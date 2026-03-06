context:
  definition:
  disabled: true
  url: "http://codebase-querier:8888/codebase-indexer/api/v1/search/definition"
  semantic:
  disabled: true
  url: "http://codebase-querier:8888/codebase-embedder/api/v1/search/semantic"
  topK: 5
  scoreThreshold: 0.5
  relation:
  disabled: true
  url: "http://codebase-querier:8888/codebase-indexer/api/v1/search/relation"
  layer: 3
  includeContent: false
  requestTimeout: 400ms
  totalTimeout: 500ms
models:
  - completionsUrl: "{{COMPLETION_BASEURL}}"
    provider: deepseek
    modelTitle: "default"
    modelName: "{{COMPLETION_MODEL}}"
    authorization: "{{COMPLETION_APIKEY}}"
    tags:
        - fastertransformer
        - deepseek
    timeout: 1000ms
    maxPrefix: 512
    maxSuffix: 50
    maxOutput: 50
    fimMode: false
    fimBegin: "<｜fim▁begin｜>"
    fimEnd: "<｜fim▁end｜>"
    fimHole: "<｜fim▁hole｜>"
    fimStop: ["<｜end▁of▁sentence｜>", "<|EOT|>", "▁<MID>"]
    tokenizerPath: "bin/deepseek-tokenizer/tokenizer.json"
    maxConcurrent: 150
    disablePrune: false
    customPruners: ["cut-single-line"]
streamController:
  maintainInterval: 600s
  completionTimeout: 2000ms
  queueTimeout: 200ms
  cleanOlderThan: 24h
wrapper:
  score:
  disabled: true
  threshold: 0.3
  syntax:
  disabled: true
  threshold: 0.5
  strPattern: ".*"
  treePattern: ".*"
  minPromptLine: 5
  endTag: "</completion>"
  prune:
  disabled: false
  pruners: ["cut-single-line"]