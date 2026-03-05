# 如何配置 Higress

本文档主要介绍如何配置 Higress AI 网关，对接用户部署的大模型。

## 1. 登录 Higress AI 网关

默认登录用户名&密码: admin/test123

## 2. 添加大模型地址

如果用户部署了新的大模型，需要添加到Costrict的模型列表，需要三步：

### 2.1. 配置`AI服务提供者`

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 服务提供者管理**。
2.  点击 **创建 AI 服务提供者**。
3.  在 **创建 AI 服务提供者** 对话框中配置大模型信息：
    * **大模型厂商**: 例如，选择 `OpenAI`。
    * **服务名称**: 自定义一个名称，如 `{{MODEL_PROVIDER}}`。
    * **协议**: 根据模型厂商选择，如 `openaiv1`。
    * **凭证**: 填入您的模型服务凭证（API Key）。如：`{{MODEL_APIKEY}}`
    * **OpenAI 服务类型**: 选择 `自定义 OpenAI 服务 BaseURL`。
    * **自定义 OpenAI 服务 BaseURL**: 填入您的模型服务基础 URL(`{{MODEL_BASEURL}}`)，**注意需要带上版本号**，例如 `https://zgsm.sangfor.com/v1/`。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_621408_2fKH133T6cdAY8_e_1751892112?w=1879&h=689&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_491553_E9UqjGwaa7i1qzHo_1751892334?w=1658&h=807&type=image/png)

### 2.2. 配置 AI 路由

AI 路由用于根据请求特征（如路径、模型名称）将请求转发到对应的 AI 服务提供者。

1.  在左侧导航栏中，选择 **AI 流量入口管理** -> **AI 路由管理**。
2.  点击 **创建 AI 路由**。
3.  在 **创建 AI 路由** 对话框中进行配置：
    * **路径 (Path)**: 配置一个前端匹配路径，例如 `/`。
    * **模型匹配规则**:
        * **Key**: `model` (表示根据请求体中的 `model` 字段进行匹配)。
        * **匹配方式**: `精确匹配`。
        * **匹配条件**: `{{MODEL_NAME}}` (具体的模型名称)。
        * 备注：也可选择“前缀匹配”，然后匹配条件设置为模型名称的某个前缀，注意大小写。
    * **目标 AI 服务**:
        * **服务名称**: 选择上一步创建的 AI 服务提供者，例如 `{{MODEL_PROVIDER}}`。

备注：上述配置的意思就是如果请求路径包含前缀'/'，且模型名称匹配本规则，则将请求路由到指定的AI服务提供者。

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_972784_ctv20hv-bBUGVzD5_1751892440?w=1895&h=691&type=image/png)

![img](https://wdcdn.qpic.cn/MTY4ODg1NTc1NDYyNDA0MA_257655_X701-MgnXRLZyoGM_1751892547?w=1698&h=858&type=image/png)

### 2.3. 配置模型列表

注：本配置项用于把用户模型展示到模型选择列表，供用户选取使用。如果未设置，用户在模型列表中无法看到新添加模型，只能通过手动输入模型全称，强行指定Costrict使用该模型。

1. 在 **插件配置** -> **AI 配额管理** 插件卡片上，点击 **配置**。

2. 切换到 **YAML 视图**，在`spec.defaultConfig.providers`下添加新模型的相关信息，如下：

```yaml
spec:
  defaultConfig:
    ...
    providers:
    - id: {{MODEL_PROVIDER}}
      models:
      - contextWindow: {{MODEL_CONTEXTSIZE}}
        description: {{MODEL_DESC}}
        maxTokens: 8192
        name: {{MODEL_NAME}}
        supportsComputerUse: true
        supportsImages: false
        supportsPromptCache: false
        supportsReasoningBudget: false
      type: {{MODEL_TYPE}}

```

