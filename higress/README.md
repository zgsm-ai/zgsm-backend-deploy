# higress

## 配置 higress 

### 服务来源

类型：DNS

名称：k8s-redis

域名列表：redis （redis服务的域名）

服务协议：http

### AI服务提供者管理

大模型供应商：openai 兼容服务

服务名称：deepseek-v3

协议：openai/v1

openai 服务类型：自定义服务

自定义 openai 服务 baseurl，如:  http://10.72.1.16:45904/model/deepseek-v3/v1

## AI 路由管理

名称：deepseek-v3

路径匹配：/

模型匹配规则：精确匹配 deepseek-v3

目标AI服务：deepseek-v3  100%

## 插件配置

### AI 配额管理

#### 编辑

镜像地址：oci://crpi-j8wrd0nl8l9v42wd.cn-shenzhen.personal.cr.aliyuncs.com/shenma-ai/ai-quota-shenma:1.0.0

插件执行阶段：默认阶段

插件优先级：750

插件拉取策略：默认策略

#### 配置

```
admin_header: "x-admin-key"
admin_key: "12345678"
admin_path: "/quota"
check_github_star: true
deduct_header: "x-quota-identity"
deduct_header_value: "user"
model_quota_weights:
  deepseek-chat: 1
redis:
  service_name: "k8s-redis.dns"
  service_port: 6379
  timeout: 2000
redis_key_prefix: "chat_quota:"
redis_used_prefix: "chat_quota_used:"
token_header: "authorization"
```

## AI 代理

### 编辑

镜像地址：oci://crpi-j8wrd0nl8l9v42wd.cn-shenzhen.personal.cr.aliyuncs.com/shenma-ai/ai-proxy-shenma:1.0.0

插件执行阶段：默认阶段

插件优先级：101

插件拉取策略：默认策略

### 配置

```
provider:
  modelMapping:
    '*': ""
    deepseek-v3: "deepseek-v3"
  type: "openai"
```

## AI 统计

#### 编辑

镜像地址：oci://crpi-j8wrd0nl8l9v42wd.cn-shenzhen.personal.cr.aliyuncs.com/shenma-ai/ai-statistics-shenma:1.0.0

插件执行阶段：默认阶段

插件优先级：900

插件拉取策略：默认策略

#### 配置

```
无
```
