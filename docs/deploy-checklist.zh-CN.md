# 部署检查清单

用于检查校验，在 Costrict 后端服务部署流程中，部署前的准备，部署中的配置以及部署后的功能。

## 一、部署前

### 1.1 后端服务器

#### 1.1.1 硬件要求

- **CPU**: Intel x64 架构，最低 16 核心
- **内存**: 最低 32GB RAM
- **存储**: 最低 512GB 可用存储空间



#### 1.1.2 软件要求

- **操作系统**: CentOS 7+ 或 Ubuntu 18.04+
- **Container Runtime**: Docker 20.10+
- **编排工具**: Docker Compose 2.0+
- **Git**：若通过离线获取 **[部署项目](https://github.com/zgsm-ai/zgsm-backend-deploy)** ,可不用



#### 1.1.3 检查

- [ ] **查看cpu**

  ```bash
  lscpu
  ```

- [ ] **查看内存**

  ```bash
  free -h
  ```

- [ ] **查看存储**

  ```bash
  df -h
  ```

- [ ] **查看操作系统**

  ```bash
  cat /etc/os-release
  ```

- [ ] **查看docker、docker-compose**

  ```bash
  docker --version
  systemctl status docker
  docker-compose --version
  ```



### 1.2 模型

#### 1.2.1 模型GPU资源（推荐）

- **对话模型**：4 * H20 或 4 * RTX4090
- **code review模型**：2 * H20 或 2 * RTX4090
- **补全模型**： 1 * H20 或 1 * RTX4090
- **embedding模型**：0.5 * H20 或 * RTX4090
- **rerank模型**：0.5 * H20 或 0.5 * RTX4090



#### 1.2.2 模型列表（推荐）

- **对话模型**： `GLM-4.5-FP8`、`GLM-4.5-106B-A12B-FP8`
- **code review模型**：`Qwen2.5-Coder-32B-Instruct`
- **补全模型**：`DeepSeek-Coder-V2-Lite-Base`
- **embedding模型**：`gte-modernbert-baseRAG/Embedding`
- **rerank模型**：`gte-reranker-modernbert-baseRAG/Rerank`

**注意**：模型是否存在密钥、APIKEY和上下文大小等限制



#### 1.2.3 检查

- [ ] **GPU资源检查**

  ```bash
  # 由模型部署方提供（AICP 或 用户）
  ```

- [ ] **模型接口**
  
  - [ ] **对话模型**: `/v1/chat/completions` 接口
  - [ ] **code review模型**: 同对话 `/v1/chat/completions` 接口
  - [ ] **补全模型**: `/v1/completions` 接口
  - [ ] **embedding模型**: `/v1/embeddings` 接口
  - [ ] **rerank模型**: `/v1/embeddings` 接口



### 1.3 后端服务

#### 1.3.1 部署项目

项目地址：https://github.com/zgsm-ai/zgsm-backend-deploy

项目存放路径：`/opt/zgsm-backend-deploy`



#### 1.3.2 服务端口要求

端口列表本地：`/opt/zgsm-backend-deploy/configure.sh`

端口列表线上：https://github.com/zgsm-ai/zgsm-backend-deploy/blob/main/configure.sh

- 端口列表：第`6~34`行



#### 1.3.3 服务镜像要求

镜像列表本地：`/opt/zgsm-backend-deploy/scripts/newest-images.list`

镜像列表线上：https://github.com/zgsm-ai/zgsm-backend-deploy/blob/main/scripts/newest-images.list



#### 1.3.4 检查

- [ ] **项目检查**

  ```bash
  ls /opt/zgsm-backend-deploy
  ```

  

- [ ] **端口检查**

  ```bash
  sudo ss -tlnp | grep -E ':(9180|9080|9091|9092|9093|2382|6379|5432|5003|9081|5000|8765|5001|9090|3000|9200|8080|8001|9001|5173|9003|9004|9005|9006|9007|9008|9009|9010|9011) '
  ```

  

- [ ] **镜像检查**

  ```bash
  bash /opt/zgsm-backend-deploy/docker-download-images.sh
  ```



## 二、部署中

### 2.1 启动配置

#### 2.1.1 模型配置

模型配置列表本地：`/opt/zgsm-backend-deploy/configure.sh`

- 大模型配置：第`71~100`行



#### 2.1.2 后端地址配置

后端地址配置列表本地：`/opt/zgsm-backend-deploy/configure.sh`

- 后端地址配置：第`143`行



#### 2.1.3 检查

- [ ] **检查文件是否存在**

  ```bash
  ls -l /opt/zgsm-backend-deploy | grep configure.sh
  ```

  

- [ ] **查看配置文件**

  ```bash
  cat /opt/zgsm-backend-deploy/configure.sh
  ```



###  2.2 执行脚本 

执行脚本：`/opt/zgsm-backend-deploy/deploy.sh`



#### 2.2.1 检查

- [ ] **检查文件是否存在以及是否具备可执行权限**

  ```bash
  ls -l /opt/zgsm-backend-deploy | grep deploy.sh
  ```



### 2.3 服务配置

#### 2.3.1 AI网关配置

AI网关配置本地：`/opt/zgsm-backend-deploy/docs/higress.zh-CN.md`



#### 2.3.2 检查

- [ ] **AI网关配置**

  ```bash
  1. 浏览器访问Higress页面
  http://{COSTRICT_BACKEND}:{PORT_HIGRESS_CONTROL}
  
  2. 查看 “AI 流量入口管理 -> AI 服务提供者管理” 页面
  
  3. 查看 “AI 流量入口管理 -> AI 路由管理” 页面
  
  4. 查看 “插件配置 -> AI 配额管理” 配置
  ```



## 三、部署后

### 3.1 服务检查

#### 3.1.1 后端服务运行

服务镜像列表本地：`/opt/zgsm-backend-deploy/scripts/newest-images.list`

服务镜像列表线上：https://github.com/zgsm-ai/zgsm-backend-deploy/blob/main/scripts/newest-images.list



#### 3.1.2 服务连通性

apisix网关服务探测接口: http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/health



#### 3.1.3 检查

- [ ] **后端服务运行检查**

  ```bash
  docker ps
  ```

  

- [ ] **后端服务网关连通性检查**

  ```bash
  curl -v http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/health
  ```



### 3.2 功能测试

#### 3.2.1 登录

登录Baseurl: {COSTRICT_BACKEND_BASEURL}



#### 3.2.2 Agent模式

- Ask
- Code
- Architect
- Debug
- Orchestrator



#### 3.2.3 CodeReview

- 文件
- 目录
- 项目



#### 3.2.4 补全

- 代码补全
- 文本补全



#### 3.2.5 检查

- [ ] **登录功能验证**
- [ ] **Agent模型功能验证**

  ````
  # Code
  ```
  在当前项目下，新增一个test.go文件，然后实现一个快排算法函数
  ```
  
  # Ask
  ```
  读取当前项目，给出项目的主要功能说明
  ```
  
  # Architect
  ```
  基于@test.go文件的内容，进行完整的排序算法设计
  ```
  
  # Debug
  ```
  检查@test.go文件中的内容，判断是排序的逻辑是否为降序
  ```
  
  # Orchestrator
  ```
  检查@test.go文件中的内容：
  1. 判断排序算法是否都存在，若不存在，则设计并实现完整的排序算法；
  2. 另外，判断是否排序算法是否都按照降序实现，若不是，则调整代码逻辑实现降序，并同时修改对应的设计文档
  ```
  ````

  
- [ ] **CodeReview功能验证**
- [ ] **补全功能验证**



### 3.3 日志检查

#### 3.3.1 服务列表

服务镜像列表本地：`/root/zgsm-backend-deploy/scripts/newest-images.list`

服务镜像列表线上：https://github.com/zgsm-ai/zgsm-backend-deploy/blob/main/scripts/newest-images.list



#### 3.3.2 检查

- [ ] **服务日志检查**

  ```bash
  docker-compose logs [service_name]
  ```
