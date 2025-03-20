# 诸葛神码部署工具(for docker-compose)

## Introduction

### Overall idea

Zhuge Shenma adopts a microservice architecture.

The entire backend system is roughly divided into three layers and four blocks. The three layers are: gateway layer, service layer, and storage layer. These three layers, plus the unified operation and maintenance center that runs through the three-layer architecture, make up the four major blocks.

#### Gateway Layer

The gateway layer is responsible for application distribution, load balancing, traffic control, and API authorization control.

- Traffic forwarding, SSL offloading: It is recommended to use Sangfor AD, or other load balancing equipment with SSL offloading capabilities.
- Application distribution, traffic control, etc.: apisix
- Login authentication, authorization control: keycloak, trampoline, kaptcha
  - User management component: keycloak
  - Login trampoline: trampoline
  - Verification code service used during the login process: kaptcha

#### Service Layer

The service layer consists of several core services, currently including:

- Proxy backend responsible for code completion: completion-server
- Proxy backend responsible for dialogue services: chat-server

The purpose of using proxy backends for both dialogue and completion is to shield the details of different model APIs and provide additional context processing capabilities.

#### Storage Layer

Storage layer:

- Relational database: pgsql
- Key-value database: etcd
- Cache: redis

#### Operation and Maintenance Center

Operation and maintenance center:

- grafana (optional)
- prometheus (optional)
- kibana (optional)
- elasticsearch (required)

## Deployment Steps

### 0. Prerequisites

#### Using your own deployed model instance

1. An X64 hardware device with a minimum configuration of 16C, 32G, 512G storage, and a graphics card that supports the operation of model inference services (at least 2 RTX4090s or 1 A800)
2. Install necessary components such as centos7, nvidia-docker, and docker-compose.

#### Using third-party API services or deploying model instances yourself

1. An X64 hardware device with a minimum configuration of 16C, 32G, 512G storage
2. Install necessary components such as centos7, docker, and docker-compose.

### 1. Modify the configuration as needed

```sh
vim configure.sh
tpl-resolve.sh
```

### 2. Download model data

### 3. Start docker-compose

```sh
docker compose up -d
```

### 4. Configure routing

```sh
apisix-*.sh
```

### 5. Import keycloak configuration

```sh
keycloak-import.sh
```

### 6. Initialize the database and create the database tables needed by chatgpt

```sh
chatgpt-initdb.sh
```

### 7. Configure the vscode-zgsm extension and adjust the server URL to the actual address
