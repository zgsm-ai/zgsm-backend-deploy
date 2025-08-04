# 神码部署工具(用于docker-compose)

## 引言

## 部署步骤

### 0. 前置条件

#### 使用自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储,配备支持模型推理服务的GPU(至少2张RTX4090或1张A800)
2. 安装CentOS 7或WSL Ubuntu,并已安装nvidia-docker、docker-compose等必要组件

#### 使用第三方API服务或自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储
2. 安装CentOS 7,已安装docker,docker-compose等必要组件

### 1. 根据需求修改配置

```sh
vim configure.sh
```

根据脚本中的说明修改配置。最重要的配置是ZGSM_BACKEND_BASEURL, ZGSM_BACKEND这两个。

### 2. 执行部署脚本

```shell
bash deploy.sh
```

### 3. 配置AI网关(higress)，对接LLM

神码后端部署完毕后，可以通过地址`http://{{ZGSM_BACKEND}}:{{PORT_AI_GATEWAY}}`，访问higress页面配置AI网关。
其中:

`{{ZGSM_BACKEND}}`, `{{PORT_AI_GATEWAY}}`的值配置在configure.sh文件中。PORT_AI_GATEWAY默认值为9000

具体请参考:

* [higress](./docs/higress.zh-CN.md)

### 4. 配置认证系统(casdoor)，对接用户的认证系统

神码后端部署完毕后，可以通过地址`http://{{ZGSM_BACKEND}}:{{PORT_CASDOOR}}`，访问神码认证系统casdoor页面，配置对接第三方认证系统。

`{{ZGSM_BACKEND}}`, `{{PORT_CASDOOR}}`的值配置在configure.sh文件中。PORT_CASDOOR默认值为9009

具体请参考：

* [casdoor](./docs/casdoor.zh-CN.md)

### 5. 在神码插件配置APISIX地址

在vscode中打开神码设置的‘提供商’页面，选择API提供商为‘诸葛神码’，在‘诸葛神码Base Url’配置部署好的后端入口URL地址，即configure.sh中配置的ZGSM_BACKEND_BASEURL变量的值。

