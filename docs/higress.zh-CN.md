# 如何配置 Higress

本文档主要介绍如何通过 `docker-compose` 和 `kubernetes` 两种方式部署和配置 Higress AI 网关。

## 一、 使用 docker-compose 部署

### 1. 安装 Higress AI 网关

首先，需要安装 Higress AI 网关。具体安装步骤可以参考官方文档：[一键部署 Higress AI 网关](https://higress.cn/ai/quick-start/)。

### 2. 配置 Redis

Redis 用于存储配额等信息。

1.  在 Higress 控制台左侧导航栏中，选择 **服务来源**。
2.  点击 **创建服务来源** 按钮。
3.  在弹出的 **创建服务来源** 对话框中，进行如下配置：
    * **类型**: 选择 `固定地址`。
    * **名称**: 输入 `local-redis`。
    * **服务地址**: 输入 Redis 的实际地址，例如 `172.31.86.242:6379`。
    * **服务协议**: 选择 `HTTP`。
4.  点击 **确定** 保存。
5.  之后可以在 **服务列表** 中看到名为 `local-redis.static` 的服务，这个地址将在后续插件配置中使用。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_347435_QBVMvq7ssanKIwxL_1751891862?w=1899&h=559&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_156901_BAKaFgMQCW8fPgQU_1751891934?w=1903&h=649&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_202352_sF5sWZvAeAVG7I1l_1751892050?w=1084&h=543&type=image/png)

### 3. 配置大模型地址

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 服务提供者管理**。
2.  点击 **创建 AI 服务提供者**。
3.  在 **创建 AI 服务提供者** 对话框中配置大模型信息：
    * **大模型厂商**: 例如，选择 `OpenAI`。
    * **服务名称**: 自定义一个名称，如 `openai`。
    * **协议**: 根据模型厂商选择，如 `openaiv1`。
    * **凭证**: 填入您的模型服务凭证（API Key）。
    * **OpenAI 服务类型**: 选择 `自定义 OpenAI 服务 BaseURL`。
    * **自定义 OpenAI 服务 BaseURL**: 填入您的模型服务基础 URL，**注意需要带上版本号**，例如 `https://zgsm.sangfor.com/v1/`。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_621408_2fKH133T6cdAY8_e_1751892112?w=1879&h=689&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_491553_E9UqjGwaa7i1qzHo_1751892334?w=1658&h=807&type=image/png)

### 4. 配置 AI 路由

AI 路由用于根据请求特征（如路径、模型名称）将请求转发到对应的 AI 服务。

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 路由管理**。
2.  点击 **创建 AI 路由**。
3.  在 **创建 AI 路由** 对话框中进行配置：
    * **路径 (Path)**: 配置一个前端匹配路径，例如 `/`。
    * **模型匹配规则**:
        * **Key**: `model` (表示根据请求体中的 `model` 字段进行匹配)。
        * **匹配方式**: `精确匹配`。
        * **Value**: `deepseek-chat` (具体的模型名称)。
    * **目标 AI 服务**:
        * **服务名称**: 选择上一步创建的 AI 服务提供者，例如 `deepseek`。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_972784_ctv20hv-bBUGVzD5_1751892440?w=1895&h=691&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_257655_X701-MgnXRLZyoGM_1751892547?w=1698&h=858&type=image/png)

### 5. 配置配额插件 (ai-quota)

#### 5.1 配置镜像地址

1.  在左侧导航栏中，选择 **插件配置**。
2.  在 AI 分类下找到 **AI 配额管理**，点击其右侧的 **编辑** (三个点图标)。
3.  在 **编辑插件** 对话框中配置：
    * **插件名称**: `ai-quota`。
    * **镜像地址**: `oci://zgsm/ai-quota-shenma:1.0.3`
    * **插件执行优先级**: `750`。
    * 可以访问 [ai-quota-shenma](https://hub.docker.com/r/zgsm/ai-quota-shenma/tags)  获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_751311_FoEtZ1Q4VKtAlUal_1751892605?w=1065&h=708&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_75970_9KmbHczNGy3tfpzU_1751892732?w=1089&h=574&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_397661_ExS-crXlHLx14vLn_1751906472?w=1748&h=1078&type=image/png)

#### 5.2 配置参数

1. 在 **AI 配额管理** 插件卡片上，点击 **配置**。

2. 切换到 **YAML 视图**，并填入以下配置：
   ```yaml
   # admin header for quota management
   admin_header: "x-admin-key"
   admin_key: "12345678"
   admin_path: "/quota"
   check_github_star: false
   # header to identify user for quota deduction
   deduct_header: "x-quota-identity"
   deduct_header_value: "user"
   # model weights for quota calculation
   model_quota_weights:
     deepseek-chat: 1
     deepseek-v3: 1
   # redis configuration
   redis:
     service_name: "local-redis.static" # 此处使用步骤2中创建的服务名
     service_port: 80
     timeout: 2000
   redis_key_prefix: "chat_quota:"
   redis_used_prefix: "chat_quota_used:"
   token_header: "authorization"
   ```

3. 打开插件开关

4. 配置含义可以参考 [ai-quota](https://github.com/zgsm-ai/higress/blob/main/plugins/wasm-go/extensions/ai-quota/README_CN.md) 插件的官方文档。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_440086_JqAdK8qPCAEgLHJA_1751893126?w=1066&h=546&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_396630_UxEOnQ-ZPcMtwz8o_1751893161?w=1246&h=647&type=image/png)

### 6. 配置代理插件 (ai-proxy)

#### 6.1 配置镜像地址

1.  在 **插件配置** 页面，找到 **AI 代理** 插件，点击 **编辑**。
2.  配置 **镜像地址**: `oci://zgsm/ai-proxy-shenma:1.0.0`。
3.  **插件执行优先级**: `100`。
4.  可以访问 [ai-proxy-shenma](https://hub.docker.com/r/zgsm/ai-proxy-shenma/tags) 获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_954241_z35DNKax3ZG7ZnDk_1751893367?w=1459&h=707&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_358724_8zC-ht4DDxaTQ7pi_1751906544?w=1781&h=1074&type=image/png)

#### 6.2 配置参数

1. 在 **AI 代理** 插件卡片上，点击 **配置**。
2. 切换到 **YAML 视图**，填入以下配置，用于模型名称的映射：
   ```yaml
   # provider configuration
   provider:
     modelMapping:
       '*': ""
       deepseek-v3: "deepseek-v3"
     type: "openai"
   ```
3. 打开插件开关
4. 配置含义可以参考 [ai-proxy](https://github.com/zgsm-ai/higress/blob/main/plugins/wasm-go/extensions/ai-proxy/README_CN.md) 插件的官方文档。

#### ![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_177409_l313Rkqi0WM6i87R_1751893532?w=1069&h=772&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_186381_jaosQ0F_CKAaFCxS_1751893555?w=1277&h=770&type=image/png)

### 7. 配置统计插件 (ai-statistics)

#### 7.1 配置镜像地址

1.  在 **插件配置** 页面，找到 **AI 统计** 插件，点击 **编辑**。
2.  配置 **镜像地址**: `oci://zgsm/ai-statistics-shenma:1.0.0`。
3.  **插件执行优先级**: `900`。
4.  可以访问 [ai-statistics-shenma](https://hub.docker.com/r/zgsm/ai-statistics-shenma/tags) 获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_136269_fsL2VZWnOapawNl__1751893715?w=1134&h=755&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_425152_nZ4GxggTTq6D4K4__1751906617?w=1768&h=1071&type=image/png)

#### 7.2 配置参数

1.  在 **AI 统计** 插件卡片上，点击 **配置**。
2.  打开插件开关。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_616133_gxddgrRsf-IkAK6M_1751893815?w=1263&h=699&type=image/png)

---

## 二、 使用 k8s 部署

### 1. 安装 Higress AI 网关

使用 `helm` 在 Kubernetes 集群中安装 Higress。

```bash
# Add higress helm repo
helm repo add higress.io [https://higress.cn/helm-charts](https://higress.cn/helm-charts)

# 安装命令，其中的 pvc 需要修改
helm install higress -n shenma higress.io/higress \
  --render-subchart-notes \
  --set higress-console.service.type=NodePort \
  --set higress-console.o11y.enabled=true \
  --set higress-console.o11y.prometheus.pvc.storageClassName=managed-nfs-storage \
  --set higress-console.o11y.grafana.pvc.storageClassName=managed-nfs-storage \
  --set higress-console.o11y.loki.pvc.storageClassName=managed-nfs-storage
```

### 2. 配置 Redis

1. 在 Higress 控制台左侧导航栏中，选择 **服务来源**。
2. 点击 **创建服务来源** 按钮。
3. 在 **创建服务来源** 对话框中，进行如下配置：
   - **类型**: 选择 `DNS域名`。
   - **名称**: 输入 `k8s-redis`。
   - **服务端口**: `6379`。
   - **域名列表**: 输入 Redis 在 k8s 集群内部的 SVC 地址，例如 `zgsm-backend-redis-master.shenma.svc.cluster.local`。
   - **服务协议**: 选择 `HTTP`。
4. 之后可以在 **服务列表** 中看到名为 `k8s-redis.dns` 的服务。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_439641_Ll_hIuBgl_Lr74Hq_1751907119?w=2234&h=1255&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_987555_mWkYKdVoJmmHPdw2_1751907196?w=2224&h=1204&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_728885_tmtRubgLF2203A_a_1751907276?w=2219&h=956&type=image/png)

### 3. 配置大模型地址

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 服务提供者管理**。
2.  点击 **创建 AI 服务提供者**。
3.  在 **创建 AI 服务提供者** 对话框中配置大模型信息：
    * **大模型厂商**: 例如，选择 `OpenAI`。
    * **服务名称**: 自定义一个名称，如 `openai`。
    * **协议**: 根据模型厂商选择，如 `openaiv1`。
    * **凭证**: 填入您的模型服务凭证（API Key）。
    * **OpenAI 服务类型**: 选择 `自定义 OpenAI 服务 BaseURL`。
    * **自定义 OpenAI 服务 BaseURL**: 填入您的模型服务基础 URL，**注意需要带上版本号**，例如 `https://zgsm.sangfor.com/v1/`。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_621408_2fKH133T6cdAY8_e_1751892112?w=1879&h=689&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_491553_E9UqjGwaa7i1qzHo_1751892334?w=1658&h=807&type=image/png)

### 4. 配置 AI 路由

AI 路由用于根据请求特征（如路径、模型名称）将请求转发到对应的 AI 服务。

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 路由管理**。
2.  点击 **创建 AI 路由**。
3.  在 **创建 AI 路由** 对话框中进行配置：
    * **路径 (Path)**: 配置一个前端匹配路径，例如 `/`。
    * **模型匹配规则**:
      * **Key**: `model` (表示根据请求体中的 `model` 字段进行匹配)。
      * **匹配方式**: `精确匹配`。
      * **Value**: `deepseek-chat` (具体的模型名称)。
    * **目标 AI 服务**:
      * **服务名称**: 选择上一步创建的 AI 服务提供者，例如 `deepseek`。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_972784_ctv20hv-bBUGVzD5_1751892440?w=1895&h=691&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_257655_X701-MgnXRLZyoGM_1751892547?w=1698&h=858&type=image/png)

### 5. 配置配额插件 (ai-quota)

#### 5.1 配置镜像地址

1.  在左侧导航栏中，选择 **插件配置**。
2.  在 AI 分类下找到 **AI 配额管理**，点击其右侧的 **编辑** (三个点图标)。
3.  在 **编辑插件** 对话框中配置：
    * **插件名称**: `ai-quota`。
    * **镜像地址**: `oci://zgsm/ai-quota-shenma:1.0.3`
    * **插件执行优先级**: `750`。
    * 可以访问 [ai-quota-shenma](https://hub.docker.com/r/zgsm/ai-quota-shenma/tags)  获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_751311_FoEtZ1Q4VKtAlUal_1751892605?w=1065&h=708&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_75970_9KmbHczNGy3tfpzU_1751892732?w=1089&h=574&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_397661_ExS-crXlHLx14vLn_1751906472?w=1748&h=1078&type=image/png)

#### 5.2 配置参数

1. 在 **AI 配额管理** 插件卡片上，点击 **配置**。

2. 切换到 **YAML 视图**，并填入以下配置。

   ```
   # admin header for quota management
   admin_header: "x-admin-key"
   admin_key: "12345678"
   admin_path: "/quota"
   check_github_star: false
   # header to identify user for quota deduction
   deduct_header: "x-quota-identity"
   deduct_header_value: "user"
   # model weights for quota calculation
   model_quota_weights:
     deepseek-chat: 1
     qwq-32b: 0
   # redis configuration for k8s
   redis:
     service_name: "k8s-redis.dns" # Use the service name created in step 2 for k8s
     service_port: 6379
     timeout: 2000
   redis_key_prefix: "chat_quota:"
   redis_used_prefix: "chat_quota_used:"
   token_header: "authorization"
   ```

3. 打开插件开关

4. 配置含义可以参考 [ai-quota](https://github.com/zgsm-ai/higress/blob/main/plugins/wasm-go/extensions/ai-quota/README_CN.md) 插件的官方文档。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_440086_JqAdK8qPCAEgLHJA_1751893126?w=1066&h=546&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_878212_JAnYrTiVn29fXyKc_1751907331?w=1883&h=1126&type=image/png)

### 6. 配置代理插件 (ai-proxy)

#### 6.1 配置镜像地址

1.  在 **插件配置** 页面，找到 **AI 代理** 插件，点击 **编辑**。
2.  配置 **镜像地址**: `oci://zgsm/ai-proxy-shenma:1.0.0`。
3.  **插件执行优先级**: `100`。
4.  可以访问 [ai-proxy-shenma](https://hub.docker.com/r/zgsm/ai-proxy-shenma/tags) 获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_954241_z35DNKax3ZG7ZnDk_1751893367?w=1459&h=707&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_358724_8zC-ht4DDxaTQ7pi_1751906544?w=1781&h=1074&type=image/png)

#### 6.2 配置参数

1. 在 **AI 代理** 插件卡片上，点击 **配置**。

2. 切换到 **YAML 视图**，填入以下配置，用于模型名称的映射：

   ```yaml
   # provider configuration
   provider:
     modelMapping:
       '*': ""
       deepseek-v3: "deepseek-v3"
     type: "openai"
   ```

3. 打开插件开关

4. 配置含义可以参考 [ai-proxy](https://github.com/zgsm-ai/higress/blob/main/plugins/wasm-go/extensions/ai-proxy/README_CN.md) 插件的官方文档。

#### ![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_177409_l313Rkqi0WM6i87R_1751893532?w=1069&h=772&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_186381_jaosQ0F_CKAaFCxS_1751893555?w=1277&h=770&type=image/png)

### 7. 配置统计插件 (ai-statistics)

#### 7.1 配置镜像地址

1.  在 **插件配置** 页面，找到 **AI 统计** 插件，点击 **编辑**。
2.  配置 **镜像地址**: `oci://zgsm/ai-statistics-shenma:1.0.0`。
3.  **插件执行优先级**: `900`。
4.  可以访问 [ai-statistics-shenma](https://hub.docker.com/r/zgsm/ai-statistics-shenma/tags) 获取最新的镜像版本。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_136269_fsL2VZWnOapawNl__1751893715?w=1134&h=755&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_425152_nZ4GxggTTq6D4K4__1751906617?w=1768&h=1071&type=image/png)

#### 7.2 配置参数

1.  在 **AI 统计** 插件卡片上，点击 **配置**。
2.  打开插件开关。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_616133_gxddgrRsf-IkAK6M_1751893815?w=1263&h=699&type=image/png)
