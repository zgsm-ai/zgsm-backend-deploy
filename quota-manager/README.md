# Quota Manager Docker Compose 部署指南

本目录包含了将 Kubernetes YAML 文件转换为 Docker Compose 格式的配置文件。

## 文件说明

- `docker-compose.yml` - 主要的 Docker Compose 配置文件
- `conf.yaml` - Quota Manager 后端配置文件
- `app.config.js` - 前端应用配置文件
- `init_db.sql` - 数据库初始化脚本

## 服务组件

### 1. PostgreSQL 数据库
- 端口：5432
- 数据库：quota_manager, auth
- 用户：keycloak
- 密码：password

### 2. Quota Manager 后端服务
- 镜像：crpi-j8wrd0nl8l9v42wd.cn-shenzhen.personal.cr.aliyuncs.com/shenma-ai/quota-manager:1.0.20
- 端口：8080
- 配置文件：/app/conf/conf.yaml

### 3. Quota Manager 前端服务
- 镜像：crpi-j8wrd0nl8l9v42wd.cn-shenzhen.personal.cr.aliyuncs.com/shenma-ai/quota-manager-frontend:1.0.7
- 端口：80
- API地址：http://localhost:8080

### 4. Higress 网关
- 镜像：higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/gateway:1.4.0
- 端口：80, 443

## 部署步骤

### 1. 启动服务
```bash
docker-compose up -d
```

### 2. 查看服务状态
```bash
docker-compose ps
```

### 3. 查看日志
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs quota-manager
docker-compose logs quota-manager-frontend
```

### 4. 停止服务
```bash
docker-compose down
```

### 5. 重新构建并启动
```bash
docker-compose up -d --build
```

## 访问地址

- 前端界面：http://localhost
- 后端API：http://localhost:8080
- 数据库：localhost:5432

## 配置说明

### 后端配置 (conf.yaml)
主要配置项：
- 数据库连接配置
- 认证数据库配置
- AI网关配置
- 服务器配置
- 调度器配置
- 凭证签名密钥
- GitHub星标检查配置
- 日志配置

### 前端配置 (app.config.js)
主要配置项：
- API基础URL
- 应用信息
- 功能开关
- 主题配置

## 网络配置

所有服务运行在 `quota-network` 网络中，子网为 `172.20.0.0/16`。

## 数据持久化

- PostgreSQL 数据：`postgres_data` 卷
- 后端日志：`quota-manager-logs` 卷
- Nginx日志：`nginx-logs` 卷

## 健康检查

所有服务都配置了健康检查：
- 后端服务：检查 `/health` 端点
- 前端服务：检查 `/health` 端点

## 故障排除

### 1. 数据库连接问题
检查 PostgreSQL 服务是否正常启动：
```bash
docker-compose logs postgres
```

### 2. 后端服务启动问题
检查后端服务日志：
```bash
docker-compose logs quota-manager
```

### 3. 前端服务启动问题
检查前端服务日志：
```bash
docker-compose logs quota-manager-frontend
```

### 4. 网络连接问题
检查网络配置：
```bash
docker network ls
docker network inspect quota-manager_quota-network
```

## 注意事项

1. 确保端口 80、443、5432、8080 未被占用
2. 首次启动时会自动创建数据库和表结构
3. 生产环境请修改默认密码和密钥
4. 根据实际需求调整资源配置
