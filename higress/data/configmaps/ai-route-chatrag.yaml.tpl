apiVersion: v1
data:
  data: '{"name":"chatrag","domains":[],"pathPredicate":{"matchType":"PRE","matchValue":"/","caseSensitive":false},"headerPredicates":[],"urlParamPredicates":[],"upstreams":[{"provider":"chatrag","weight":100,"modelMapping":{}}],"modelPredicates":[{"matchType":"EQUAL","matchValue":"{{CHAT_DEFAULT_MODEL}}"}],"authConfig":{"enabled":false},"fallbackConfig":{"enabled":false}}'
kind: ConfigMap
metadata:
  creationTimestamp: "2025-09-06T03:20:26Z"
  labels:
    higress.io/config-map-type: ai-route
    higress.io/resource-definer: higress
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:data:
        .: {}
        f:data: {}
      f:metadata:
        f:labels:
          .: {}
          f:higress.io/config-map-type: {}
          f:higress.io/resource-definer: {}
    manager: Kubernetes Java Client
    operation: Update
    time: "2025-09-06T03:20:26Z"
  name: ai-route-chatrag
  namespace: higress-system
  resourceVersion: "1"
