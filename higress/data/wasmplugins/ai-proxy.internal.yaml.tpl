apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  annotations:
    higress.io/comment: PLEASE DO NOT EDIT DIRECTLY. This resource is managed by Higress.
    higress.io/wasm-plugin-title: AI Proxy
  creationTimestamp: null
  labels:
    higress.io/internal: "true"
    higress.io/resource-definer: higress
    higress.io/wasm-plugin-built-in: "true"
    higress.io/wasm-plugin-category: ai
    higress.io/wasm-plugin-name: ai-proxy
    higress.io/wasm-plugin-version: 1.0.0
  managedFields:
  - apiVersion: extensions.higress.io/v1alpha1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          f:higress.io/comment: {}
        f:labels:
          f:higress.io/internal: {}
      f:spec:
        f:defaultConfig:
          f:providers: {}
        f:matchRules: {}
        f:url: {}
    manager: Kubernetes Java Client
    operation: Update
    time: "2025-08-06T09:34:36Z"
  name: ai-proxy.internal
  namespace: higress-system
  resourceVersion: "4"
spec:
  defaultConfig:
    providers:
    - apiTokens:
      - YOUR_OLLAMA_API_KEY
      id: ollama
      ollamaServerHost: YOUR_OLLAMA_SERVER_HOST
      ollamaServerPort: 11434
      type: ollama
    - failover:
        enabled: false
      apiTokens:
      - {{CHAT_APIKEY}}
      id: chatrag
      openaiCustomUrl: {{CHAT_BASEURL}}/v1
      openaiExtraCustomUrls: []
      retryOnFailure:
        enabled: false
      type: openai
  defaultConfigDisable: false
  failStrategy: FAIL_OPEN
  matchRules:
  - config:
      activeProviderId: chatrag
    configDisable: false
    service:
    - llm-chatrag.internal.static
  - config:
      activeProviderId: ollama
    configDisable: false
    service:
    - llm-ollama.internal.dns
  priority: 100
  url: http://portal:80/wasm/ai-proxy.wasm
status: {}
