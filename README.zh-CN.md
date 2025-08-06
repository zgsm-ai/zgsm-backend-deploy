# Costrict部署工具(用于docker-compose)

## 引言

## 部署步骤

### 0. 前置条件

#### 使用自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储,配备支持模型推理服务的GPU(至少2张RTX4090或1张A800)
2. 安装CentOS 7或WSL Ubuntu,并已安装nvidia-docker、docker-compose等必要组件

#### 使用第三方API服务或自部署模型实例

1. X64硬件设备,最低配置16C、32G、512G存储
2. 安装CentOS 7,已安装docker,docker-compose等必要组件

#### 准备部署脚本

下载Costrict后端部署项目(for docker-compose):

```sh
git clone https://github.com/zgsm-ai/zgsm-backend-deploy.git
cd zgsm-backend-deploy
```

### 1. 根据需求修改配置

```sh
vim configure.sh
```

根据脚本中的说明修改配置。最重要的配置是COSTRICT_BACKEND_BASEURL, COSTRICT_BACKEND这两个。

### 2. 执行部署脚本

```shell
bash deploy.sh
```

### 3. 配置AI网关(higress)，对接LLM

Costrict后端部署完毕后，可以通过地址`http://{{COSTRICT_BACKEND}}:{{PORT_HIGRESS_CONTROL}}`，访问higress页面配置AI网关。
其中:

`{{COSTRICT_BACKEND}}`, `{{PORT_HIGRESS_CONTROL}}`的值配置在configure.sh文件中。PORT_HIGRESS_CONTROL默认值为8001

具体请参考:

* [higress](./docs/higress.zh-CN.md)

### 4. 配置认证系统(casdoor)，对接用户的认证系统

Costrict后端部署完毕后，可以通过地址`http://{{COSTRICT_BACKEND}}:{{PORT_CASDOOR}}`，访问Costrict认证系统casdoor页面，配置对接第三方认证系统。

`{{COSTRICT_BACKEND}}`, `{{PORT_CASDOOR}}`的值配置在configure.sh文件中。PORT_CASDOOR默认值为9009

如果仅仅进行测试验证，可以无需配置第三方认证系统，使用预置的默认账号demo进行登录试用。

```
账号： demo
密码： test123
```

具体请参考：

* [casdoor](./docs/casdoor.zh-CN.md)

### 5. 在vscode的Costrict扩展配置Costrict后端入口地址

Costrict后端的入口地址，默认为`http://{{COSTRICT_BACKEND}}:{{PORT_APISIX_ENTRY}}`。

`{{COSTRICT_BACKEND}}`, `{{PORT_APISIX_ENTRY}}`的值配置在configure.sh文件中。PORT_APISIX_ENTRY默认值为9080。

如果配置有域名服务器，前置应用发布/负载均衡等设备，可以通过这些设备把Costrict后端BASEURL(假设是https://sample.com)绑定到`http://{{COSTRICT_BACKEND}}:{{PORT_APISIX_ENTRY}}`。部署时，需要把configure.sh文件中COSTRICT_BACKEND_BASEURL变量的值设为该地址(比如：COSTRICT_BACKEND_BASEURL="https://sample.com")。

Costrict后端部署完成后，需要配置vscode Costrict扩展的`Costrict Base Url`。
在vscode中打开Costrict设置的‘提供商’页面，选择API提供商为‘Costrict’，在‘Costrict Base Url’配置部署好的后端入口URL地址，即configure.sh中配置的COSTRICT_BACKEND_BASEURL变量的值。
然后，点击‘登录Costrict’,使用认证系统许可的账号，或者预设的demo账号进行登录。

接下来，就可以开始使用`Costrict+私有化部署后端`进行开发了！

祝您享受AI赋能开发的快乐！
