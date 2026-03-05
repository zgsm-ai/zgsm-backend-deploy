# 部署常见问题解答

本文档记录了 CoStrict 后端服务部署过程中的常见问题及其解决方法。

## 一、后端服务镜像下载问题

### 问题1：如何下载后端服务镜像？

**处理方法**：

当前提供两种下载方式：
1. **Docker Hub**：部署服务器若能访问 Docker Hub，建议直接使用第一种方式下载。
2. **百度云盘**：部署服务器若无法访问 Docker Hub，选择一台能访问百度云盘的电脑，将百度云盘中的镜像下载到本机，然后传入到部署服务器中。

### 问题2：使用 **Docker Hub** 方式下载镜像超时失败

**处理方法**：

可能因为外网问题导致访问镜像超时失败。可以通过修改镜像源，使得镜像能正常下载。

> 修改 `docker` 镜像源
```bash
# 编辑文件: /etc/docker/daemon.json，添加以下内容
{
    "registry-mirrors": [
       "https://docker.m.daocloud.io",
       "https://docker.imgdb.de",
       "https://docker-0.unsee.tech",
       "https://docker.hlmirror.com",
       "https://cjie.eu.org"
    ]
}

# 重启docker服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 二、ARM架构机器部署问题

### 问题：ARM架构机器部署失败

**处理方法**：

当前私有化部署项目支持 AMD 架构机器部署，建议更换成 AMD 架构的机器部署。

---

## 三、Docker相关问题

### 问题：在执行 `deploy.sh` 一键部署时提示 `docker` 命令执行错误

**处理方法**：

检查部署服务器上是否存在 `docker` 和 `docker-compose` 命令，以及版本是否过低。推荐版本：
- **Docker**：20.10.24
- **Docker Compose**：v2.39.3

---

## 四、端口占用问题

### 问题：端口占用

**处理方法**：

1. 连接到后端部署服务器上，cd 到部署项目目录下
2. 使用部署检查清单中的端口检查命令，查看具体哪些端口被占用
3. vi 编辑 `configure.sh` 修改被占用端口为其他未使用的端口，保存 `configure.sh`
4. 停止删除掉部署项目涉及的容器，并清理掉错误的数据
5. 重新执行 deploy.sh 脚本一键部署

> 端口检查命令
```bash
sudo ss -tlnp | grep -E ':(39180|39080|32382|36379|35432|35003|39090|33000|39200|38001|39009) '
```

> 停止删除部署项目涉及容器命令
```bash
# 方式1：通过docker-compose停止
docker-compose down

# 方式2：通过脚本停止
bash scripts/remove-containers.sh -f scripts/images.list
```

> 清理错误数据命令
```bash
bash scripts/clean-storage.sh
```

---

## 五、用户登录相关问题

### 问题1：初始登录账号失败

**处理方法**：

通过部署项目部署的 CoStrict 服务，有提供一个默认测试账号：
- **用户名**: demo
- **密码**: test123

登录时，请选择 **"密码"** 方式登录

### 问题2：账号登录提示客户端ID或密钥错误

**原因**：

在部署时，由于系统资源、性能方面问题，导致在进行 `postgres` 表的初始记录写入时失败

**处理方法**：

1. 访问 `casdoor` 页面，点击 **"身份认证"** 进入应用页面
2. 选择名称为 **"loginApp"** 记录中的 **"操作"** 列的 **"编辑"** 按钮进入编辑页面
3. 找到客户端配置（`客户端ID`、`客户端密钥`）进行修改，修改内容：部署项目目录下 `configure.sh` 文件中的配置（`OIDC_AUTH_CLIENT_ID`、`OIDC_AUTH_CLIENT_SECRET`）

**注意**：当前方式只处理了客户端ID和密钥配置缺失的问题，其他postgres表初始记录缺少可能会导致其他问题

**建议**： 
> 方式1：

使用符合部署要求的服务器重新部署

> 方式2：

连接到当前的后端部署服务器上，cd到部署项目目录下，对比 `posgres/scripts` 下sql文件内容和 `postgres容器` 内表记录并补充

### 问题3：账号登录提示回调URL错误

**原因**：

在部署时，由于系统资源、性能方面问题，导致在进行 `postgres` 表的初始记录写入时失败

**处理方法**：

1. 访问 `casdoor` 页面，点击 **"身份认证"** 进入应用页面
2. 选择名称为 **"loginApp"** 记录中的 **"操作"** 列的 **"编辑"** 按钮进入编辑页面
3. 找到重定向URLs配置（`重定向URLs`）进行修改，修改内容： `http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/oidc-auth/api/v1/plugin/login/callback`

**注意**：当前方式只处理了回调URL配置缺失的问题，其他postgres表初始记录缺少可能会导致其他问题

**建议**：
> 方式1：

使用符合部署要求的服务器重新部署

> 方式2：

连接到当前的后端部署服务器上，cd到部署项目目录下，对比 `posgres/scripts` 下sql文件内容和 `postgres容器` 内表记录并补充

### 问题4：如何新增用户

**处理方法**：

1. 访问 `casdoor` 页面，点击 **"用户管理"** 进入组织页面
2. 选择名称为 **"user-group"** 记录中 **"操作"** 列的 **"用户"** 按钮进入 **"user-group"** 的用户页面
3. 点击 **"添加"** 按钮添加新用户

### 问题5：新增用户登录失败

**问题详情**：
```
code:oidc-auth.updateInfoFailed,data:"",message:"update user info fail:faile to create user:faile to create:ERROR: duplicate key value violate unique constraint \"idx_auth_users_github_id\"(SQLSTATE 23505)
```

**处理方法**：

1. 连接到后端部署服务器上，cd 到部署项目目录下
2. 使用 `docker` 命令连接到 `postgres` 服务容器内
3. 连接 `postgres` 服务后，执行以下操作：
   - 切换 db 到 auth：`\c auth;`
   - 删除唯一索引：`drop index idx_auth_users_github_id;`
4. 操作完成后，在 `CoStrict` 插件使用新增用户重新登录

### 问题6：用户认证过期

**问题详情**：
```
API请求失败
错误详情:
认证已过期
认证时间:11/3/2025,11:32:55 AM
过期时间:11/10/2025,11:32:55 AM
```

**处理方法**：

点击CoStrict插件右上角账户头像进入账户界面，点击 **"重新登录"** 进行登录。

### 问题7：如何修改用户认证有效期长度

**处理方法**：

1. 访问casdoor页面，点击 **"身份认证"** 进入应用页面
2. 选择名称为 **"loginApp"** 记录中的 **"操作"** 列的 **"编辑"** 按钮进入编辑页面
3. 找到认证Token过期配置（`Access Token过期`、`Refresh Token过期`）进行修改

### 问题8：账户界面访问网页错误

**问题详情**：

在账户界面点击 **"购买更多配额"**、**"参与运营活动获取配额"** 和 **"查看账户详情"** 后访问的网页存在错误。

**处理方法**：

私有化部署，不涉及配额使用，忽略即可。

---

## 六、模型更新问题

### 问题1：对话模型更新

**处理方法**：

1. 访问 `higress` 页面，到以下三个页面查看并配置：
   - **AI网关管理->AI服务提供者管理**：配置模型访问信息
   - **AI网关管理->AI路由管理**：配置模型路由信息
   - **插件配置->AI配额管理**：配置 `CoStrict` 插件可选的模型信息
2. 修改完成后，在 `CoStrict` 插件点击 **设置->供应商**，点击 **"刷新模型"**

### 问题2：代码补全模型更新

**处理方法**：

1. 连接到后端部署服务器上，cd 到部署项目目录下
2. vi 编辑 `docker-compose.yml`，修改 **code-completion** 服务的配置（`OPENAI_MODEL_HOST`、`OPENAI_MODEL`、`OPENAI_MODEL_AUTHORIZATION`）
3. 保存 `docker-compose.yml`
4. 停止并删除掉 **code-completion** 服务容器
5. 基于更新后的 `docker-compose.yml` 文件重新启动 **code-completion** 服务容器

> 停止并删除掉 **code-completion** 服务容器
```bash
docker stop code-completion
docker rm code-completion
```

> 基于更新后的 `docker-compose.yml` 文件重新启动 **code-completion** 服务容器
```bash
# 在部署项目目录下执行命令
docker-compose up -d
```

### 问题3：Embedding、Rerank模型更新

**处理方法**：

1. 连接到后端部署服务器上，cd 到部署项目目录下
2. vi 编辑 `codebase-embedder/conf.yaml`，分别修改 **VectorStore** 下的 **Embedder** 和 **Reranker** 部分配置（`Model`、`ApiKey`、`ApiBase`）
3. 保存 `codebase-embedder/conf.yaml`
4. 停止并删除掉 **codebase-embedder** 服务容器
5. 基于更新后的 `codebase-embedder/conf.yaml` 配置文件使用 `docker-compose.yml` 文件重新启动 **codebase-embedder** 服务容器

> 停止并删除掉 **codebase-embedder** 服务容器
```bash
docker stop codebase-embedder
docker rm codebase-embedder
```

> 基于更新后的 `codebase-embedder/conf.yaml` 配置文件使用 `docker-compose.yml` 文件重新启动 **codebase-embedder** 服务容器
```bash
# 在部署项目目录下执行命令
docker-compose up -d
```

### 问题4：higress中更新了对话模型列表，但CoStrict插件刷新模型列表还是旧的

**原因分析1**：

可能由于网络或代理问题，导致访问后端服务失败

**处理方法**：

使用浏览器访问 `http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/ai-gateway/api/v1/models` 能否获取到模型列表

**原因分析2**：

可能由于 `higress` 中的配置存在问题，使得 `higress` 部分插件没有启动成功，导致配置没有生效

**处理方法**：

1. 连接到后端部署服务器上, docker 命令进入 `higress` 容器内
2. cd到 `/var/log/higress` 目录下， 查看 `gateway.log` 日志内容

### 问题5：新增的模型支持图片，如何配置使CoStrict支持图片消息

**处理方法**：

1. 首先得确定模型具备支持图片的能力
2. 访问 `higress` 页面，到 **插件配置->AI配额管理**
3. 点击 **"配置"** 进入配置页面，选择 **"YAML视图"** 展示yaml格式，在配置项 **providers** 中找到支持图片的模型配置部分，修改其中配置 `supportsImages` 为 `true`
4. 修改完成后，在 `CoStrict` 插件点击 **设置->供应商**，点击 **"刷新模型"**

---

## 七、对话相关错误

### 问题1：对话报错

**问题详情**：
```
API请求失败
错误详情:
zgsm completion error: Connection error
```

**处理方法**：

当前报错表明：没有访问到部署服务的服务器。可能本机存在代理相关问题，建议检查本机的代理等网络问题。

### 问题2：简单对话可以用，但几轮对话就出现对话失败

**处理方法**：

可能是当前选择模型支持的上下文长度较小，建议选择支持 **64k+** 的模型。

---

## 八、Strict模式相关错误

### 问题：`Strict` 模式生成文件不在指定目录

**处理方法**：

`Strict` 模型对模型能力要求较高，可能当前选择模型的指令遵循能力不足，建议选择 **`glm-4.5` 或以上** 的模型。

---

## 九、杀毒软件相关警告

### 问题：电脑杀毒软件监测到 `codebase-indexer.exe` 或 `costrict.exe`为病毒

**处理方法**：

这两个服务为 `CoStrict` 插件在电脑上的客户端程序，建议修改杀毒软件允许其运行。