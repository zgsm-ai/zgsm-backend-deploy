apiVersion: networking.higress.io/v1
kind: McpBridge
metadata:
  creationTimestamp: "2000-01-01T00:00:00Z"
  managedFields:
  - apiVersion: networking.higress.io/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:spec:
        f:registries: {}
    manager: Kubernetes Java Client
    operation: Update
    time: "2025-08-06T09:30:36Z"
  name: default
  namespace: higress-system
  resourceVersion: "3"
spec:
  registries:
  - domain: 127.0.0.1:8001
    name: higress-console
    port: 80
    type: static
  - domain: YOUR_OLLAMA_SERVER_HOST
    name: llm-ollama.internal
    port: 11434
    protocol: http
    type: dns
  - domain: {{COSTRICT_BACKEND}}:6379
    name: local-redis
    port: 80
    protocol: http
    type: static
  - domain: {{CHAT_MODEL_HOST}}
    name: llm-chatrag.internal
    port: 80
    protocol: http
    type: static
  - domain: {{CODEREVIEW_MODEL_HOST}}
    name: llm-codereview.internal
    port: 80
    protocol: http
    type: static
status: {}
