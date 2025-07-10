# 神码部署工具(用于docker-compose)

## 引言

### 整体架构

神码采用微服务架构。

后系统分为三层四构成。三层分别是: Gateway层、Service层、Storage层。这三层外加横跨三层的统一运维中心构成了四种主要构成。

#### 网关层(Gateway层)

网关层负责应用分发、负载均衡、流量控制及API授权控制。

- 流量转发,SSL卸载: 推荐使用深信服AD,也可以使用其他具备SSL卸载能力的负载均衡设备
- 应用分发、流量控制等: APISIX
- 登录认证、授权控制: Keycloak, Trampoline, Kaptcha
  - 用户管理组件: Keycloak
  - 登录跳板: Trampoline
  - 登录过程中所使用的验证码服务: Kaptcha

#### 服务层(Service层)

服务层由若干个核心服务组成,目前包括:

- 负责代码补全的代理后端: completion-server
- 负责聊天服务的代理后端: chat-server

chat和completion都使用代理后端的原因是为了屏蔽不同模型API的细节并额外提供上下文处理能力。

#### 存储层(Storage层)

存储层:

- 关系型数据库: PostgreSQL
- 键值数据库: etcd
- 缓存: Redis

#### 运维中心

运维中心:

- Grafana(可选)
- Prometheus(可选)
- Kibana(可选)
- Elasticsearch(必需)

## 部署步骤

### 0. 前置条件

#### 使用自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储,配备支持模型推理服务的GPU(至少2张RTX4090或1张A800)
2. 安装CentOS 7或WSL Ubuntu,并已安装nvidia-docker、docker-compose等必要组件

#### 使用第三方API服务或自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储
2. 安装CentOS 7,已安装docker,docker-compose等必要组件

### 1. 按要求修改配置

```sh
vim configure.sh
```

根据脚本中的说明修改配置。最重要的配置是ZGSM_BACKEND_BASEURL, ZGSM_BACKEND这两个。

### 2. 执行部署脚本

```shell
bash deploy.sh
```

### 3. 配置AI网关(higress)，对接LLM

神码后端部署完毕后，可以通过地址http://{{ZGSM_BACKEND}}:{{PORT_AI_GATEWAY}}，访问higress页面配置AI网关。
其中:

`{{ZGSM_BACKEND}}`, `{{PORT_AI_GATEWAY}}`的值配置在configure.sh文件中。

具体请参考:

* [higress](./docs/higress.zh-CN.md)

### 4. 配置认证系统(casdoor)，对接用户的认证系统

神码后端部署完毕后，可以通过地址http://{{ZGSM_BACKEND}}:{{PORT_CASDOOR}}，访问神码认证系统casdoor页面，配置对接第三方认证系统。

`{{ZGSM_BACKEND}}`, `{{PORT_CASDOOR}}`的值配置在configure.sh文件中。

具体请参考：

* [casdoor](./docs/casdoor.zh-CN.md)

### 5. 在神码插件配置APISIX地址

在vscode中打开神码设置的‘提供商’页面，选择API提供商为‘诸葛神码’，在‘诸葛神码Base Url’配置部署好的后端入口URL地址，即configure.sh中配置的ZGSM_BACKEND_BASEURL变量的值。

