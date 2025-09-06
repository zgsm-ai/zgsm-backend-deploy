apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    higress.io/comment: PLEASE DO NOT EDIT DIRECTLY. This resource is managed by Higress.
    higress.io/destination: llm-chatrag.internal.static:80
    higress.io/exact-match-header-x-higress-llm-model: {{CHAT_DEFAULT_MODEL}}
    higress.io/ignore-path-case: "true"
  creationTimestamp: "2025-09-06T03:20:26Z"
  labels:
    higress.io/domain_higress-default-domain: "true"
    higress.io/internal: "true"
    higress.io/resource-definer: higress
  managedFields:
  - apiVersion: networking.k8s.io/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .: {}
          f:higress.io/comment: {}
          f:higress.io/destination: {}
          f:higress.io/exact-match-header-x-higress-llm-model: {}
          f:higress.io/ignore-path-case: {}
        f:labels:
          .: {}
          f:higress.io/domain_higress-default-domain: {}
          f:higress.io/internal: {}
          f:higress.io/resource-definer: {}
      f:spec:
        f:ingressClassName: {}
        f:rules: {}
    manager: Kubernetes Java Client
    operation: Update
    time: "2025-09-06T03:20:26Z"
  name: ai-route-chatrag.internal
  namespace: higress-system
  resourceVersion: "1"
spec:
  ingressClassName: higress
  rules:
  - http:
      paths:
      - backend:
          resource:
            apiGroup: networking.higress.io
            kind: McpBridge
            name: default
        path: /
        pathType: Prefix
status:
  loadBalancer: {}
