# Shenma Deployment Tool (for docker-compose)

## Introduction

### Overall Architecture

Shenma adopts a microservice architecture.

The backend system is divided into three layers and four components. The three layers are: Gateway Layer, Service Layer, and Storage Layer. These three layers, plus the unified Operation & Maintenance Center that spans all layers, form the four major components.

#### Gateway Layer

The Gateway Layer is responsible for application distribution, load balancing, traffic control, and API authorization control.

- Traffic forwarding, SSL offloading: Sangfor AD is recommended, but other load balancing devices with SSL offloading capabilities can also be used
- Application distribution, traffic control, etc.: APISIX
- Login authentication, authorization control: Keycloak, Trampoline, Kaptcha
  - User management component: Keycloak
  - Login trampoline: Trampoline
  - CAPTCHA service used in the login process: Kaptcha

#### Service Layer

The Service Layer consists of several core services, currently including:

- Proxy backend responsible for code completion: completion-server
- Proxy backend responsible for chat services: chat-server

For both chat and completion, the purpose of using proxy backends is to shield the details of different model APIs and provide additional context processing capabilities.

#### Storage Layer

Storage Layer:

- Relational database: PostgreSQL
- Key-value database: etcd
- Cache: Redis

#### Operation & Maintenance Center

Operation & Maintenance Center:

- Grafana (optional)
- Prometheus (optional)
- Kibana (optional)
- Elasticsearch (required)

## Deployment Steps

### 0. Prerequisites

#### Using self-deployed model instances

1. An X64 hardware device with a minimum configuration of 16C, 32G, 512G storage, equipped with a GPU that supports model inference services (at least 2 RTX4090 or 1 A800)
2. CentOS 7 or WSL Ubuntu installed with necessary components such as nvidia-docker, docker-compose, etc.

#### Using third-party API services or self-deploying model instances

1. An X64 hardware device with a minimum configuration of 16C, 32G, 512G storage
2. CentOS 7 installed with docker, docker-compose, and other necessary components

### 1. Modify configuration according to requirements

```sh
vim deploy.sh
vim configure.sh
```

### 2. Execute the deployment script
```shell
bash deploy.sh
```

### 3. Configure LLM API keys in the One-API backend
     Default address is http://localhost:30000, default account is root, password is 123456.
     Click on "Channels", add a new channel, select the LLM provider, fill in the name and key, other fields can be left empty.

### 4. Configure APISIX address in Shenma plugin
    Shenma baseurl: Default is http://{local machine IP}:8090/v1 (Note: Using localhost may cause issues, it's recommended to use ipconfig to get the actual IP address).

---

## Kubernetes Helm Deployment

For production or large-scale environments, you can deploy using Kubernetes Helm charts.

**See detailed instructions here:**

[Helm Chart Deployment Guide](kubernetes/helm/README.md)

