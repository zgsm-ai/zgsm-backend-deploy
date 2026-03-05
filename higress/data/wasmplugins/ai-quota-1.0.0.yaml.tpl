apiVersion: extensions.higress.io/v1alpha1
kind: WasmPlugin
metadata:
  annotations:
    higress.io/wasm-plugin-description: Implement quota-based rate limiting according
      to assigned fixed quotas, while also supporting quota management capabilities,
      including querying, refreshing, and adjusting quotas.
    higress.io/wasm-plugin-icon: https://img.alicdn.com/imgextra/i1/O1CN018iKKih1iVx287RltL_!!6000000004419-2-tps-42-42.png
    higress.io/wasm-plugin-title: AI Quota
  creationTimestamp: "2025-08-06T09:33:15Z"
  labels:
    higress.io/resource-definer: higress
    higress.io/wasm-plugin-built-in: "true"
    higress.io/wasm-plugin-category: ai
    higress.io/wasm-plugin-name: ai-quota
    higress.io/wasm-plugin-version: 1.0.0
  managedFields:
  - apiVersion: extensions.higress.io/v1alpha1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .: {}
          f:higress.io/wasm-plugin-description: {}
          f:higress.io/wasm-plugin-icon: {}
          f:higress.io/wasm-plugin-title: {}
        f:labels:
          .: {}
          f:higress.io/resource-definer: {}
          f:higress.io/wasm-plugin-built-in: {}
          f:higress.io/wasm-plugin-category: {}
          f:higress.io/wasm-plugin-name: {}
          f:higress.io/wasm-plugin-version: {}
      f:spec:
        f:defaultConfig:
          .: {}
          f:admin_header: {}
          f:admin_key: {}
          f:admin_path: {}
          f:providers: {}
          f:quota_management:
            .: {}
            f:admin_quota_path: {}
            f:cache_ttl_seconds: {}
            f:deduct_header: {}
            f:deduct_header_value: {}
            f:deduct_req_num: {}
            f:redis_key_prefix: {}
            f:redis_quota_prefix: {}
            f:redis_used_prefix: {}
            f:user_level_enabled: {}
          f:redis:
            .: {}
            f:service_name: {}
            f:service_port: {}
            f:timeout: {}
          f:token_header: {}
        f:defaultConfigDisable: {}
        f:failStrategy: {}
        f:priority: {}
        f:url: {}
    manager: Kubernetes Java Client
    operation: Update
    time: "2025-09-06T02:33:05Z"
  name: ai-quota-1.0.0
  namespace: higress-system
  resourceVersion: "4"
spec:
  defaultConfig:
    admin_header: x-admin-key
    admin_key: "12345678"
    admin_path: /quota
    providers:
    - id: zhipu-provider
      models:
      - contextWindow: {{CHAT_MODEL_CONTEXTSIZE}}
        description: {{CHAT_MODEL_DESC}}
        maxTokens: 8192
        name: {{CHAT_DEFAULT_MODEL}}
        supportsComputerUse: true
        supportsImages: false
        supportsPromptCache: false
        supportsReasoningBudget: false
      type: zhipu
    quota_management:
      admin_quota_path: /check-quota
      cache_ttl_seconds: 5
      deduct_header: x-quota-identity
      deduct_header_value: user
      deduct_req_num: 10
      redis_key_prefix: 'chat_quota:'
      redis_quota_prefix: 'quota_check:'
      redis_used_prefix: 'chat_quota_used:'
      user_level_enabled: false
    redis:
      service_name: local-redis.static
      service_port: 80
      timeout: 2000
    token_header: authorization
  defaultConfigDisable: false
  failStrategy: FAIL_OPEN
  priority: 750
  url: http://portal:80/wasm/ai-quota.wasm
status: {}
