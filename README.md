# Costrict Backend Deployment Tool

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://docs.docker.com/get-docker/)
[![Docker Compose](https://img.shields.io/badge/docker--compose-required-blue.svg)](https://docs.docker.com/compose/install/)

## Project Overview

Costrict Backend Deployment Tool is an enterprise-level AI code assistant backend service deployment solution based on Docker Compose. This project provides a complete microservice architecture, including core components such as AI gateway, identity authentication, code analysis, and chat services, supporting both private deployment and cloud service modes.

### Core Features

- **Microservice Architecture**: Containerized distributed service architecture
- **AI Gateway Integration**: Support for multiple large language model access
- **Identity Authentication System**: Integrated with Casdoor for enterprise-level identity management
- **Intelligent Code Analysis**: Provides code review, completion, optimization and other functions
- **Scalable Design**: Support for horizontal scaling and custom plugins

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  VSCode Plugin  │────│   API Gateway   │────│ Backend Services│
│   (Costrict)    │    │ (Apache APISIX) │    │ (Microservices) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │                        │
                        ┌─────────────────┐    ┌─────────────────┐
                        │   AI Gateway    │    │ Database Cluster│
                        │   (Higress)     │    │   (PostgreSQL)  │
                        └─────────────────┘    └─────────────────┘
```

## System Requirements

### Self-deployed Model Instance Environment

**Hardware Requirements**:
- CPU: Intel x64 architecture, minimum 16 cores
- Memory: Minimum 32GB RAM
- Storage: Minimum 512GB available storage space
- GPU: CUDA-enabled graphics card (Recommended for code completion/analysis: 2×RTX 4090 or 1×A800, Recommended for chat model: 8*H20)

**Software Requirements**:
- Operating System: CentOS 7+ or Ubuntu 18.04+ (WSL supported)
- Container Runtime: Docker 20.10+
- Orchestration Tool: Docker Compose 2.0+
- NVIDIA Driver: nvidia-docker support

### Third-party API Service Environment

**Hardware Requirements**:
- CPU: Intel x64 architecture, minimum 16 cores
- Memory: Minimum 32GB RAM
- Storage: Minimum 512GB available storage space

**Software Requirements**:
- Operating System: CentOS 7+ or Ubuntu 18.04+
- Container Runtime: Docker 20.10+
- Orchestration Tool: Docker Compose 2.0+

## Quick Start

### 1. Get Deployment Code

```bash
git clone https://github.com/zgsm-ai/zgsm-backend-deploy.git
cd zgsm-backend-deploy
```

### 2. Environment Configuration

Edit the configuration file:

```bash
vim configure.sh
```

**Key Configuration Parameters**:

| Parameter Name | Description | Default Value | Required |
|---------|------|--------|----------|
| `COSTRICT_BACKEND_BASEURL` | Backend service base URL | - | ✅ |
| `COSTRICT_BACKEND` | Backend service host address | - | ✅ |
| `PORT_APISIX_ENTRY` | API gateway entry port | 9080 | ❌ |
| `PORT_HIGRESS_CONTROL` | Higress console port | 8001 | ❌ |
| `PORT_CASDOOR` | Casdoor authentication system port | 9009 | ❌ |

Model Settings:

| Parameter Name | Description | Default Value | Required |
|---------|------|--------|----------|
| `CHAT_MODEL_HOST` | IP+PORT of chat model | - | ✅ |
| `CHAT_BASEURL` | Access address of chat model | - | ✅ |
| `CHAT_DEFAULT_MODEL` | Name of chat model | - | ✅ |
| `CHAT_MODEL_CONTEXTSIZE` | Context length of chat model | - | ✅ |
| `CHAT_MODEL_DESC` | Description of chat model | - | ❌ |
| `CHAT_APIKEY` | APIKEY of chat model, required if the model enables APIKEY authentication | - | ❌ |
| `CODEREVIEW_MODEL_HOST` | IP+PORT of Codereview model | - | ✅ |
| `CODEREVIEW_BASEURL` | Access address of Codereview model | - | ✅ |
| `CODEREVIEW_MODEL` | Name of Codereview model | - | ✅ |
| `CODEREVIEW_MODEL_CONTEXTSIZE` | Context length of Codereview model | - | ✅ |
| `CODEREVIEW_MODEL_DESC` | Description of Codereview model | - | ❌ |
| `CODEREVIEW_APIKEY` | APIKEY of Codereview model, required if the model enables APIKEY authentication | - | ❌ |
| `COMPLETION_BASEURL` | Access address of code completion model | - | ✅ |
| `COMPLETION_MODEL` | Name of code completion model | - | ✅ |
| `COMPLETION_APIKEY` | APIKEY of code completion model, required if the model enables APIKEY authentication | - | ❌ |
| `EMBEDDER_BASEURL` | Access address of vector embedding model | - | ✅ |
| `EMBEDDER_MODEL` | Name of vector embedding model | - | ✅ |
| `EMBEDDER_APIKEY` | APIKEY of vector embedding model, required if the model enables APIKEY authentication | - | ❌ |
| `RERANKER_BASEURL` | Access address of rerank model | - | ✅ |
| `RERANKER_MODEL` | Name of rerank model | - | ✅ |
| `RERANKER_APIKEY` | APIKEY of rerank model, required if the model enables APIKEY authentication | - | ❌ |

Note: Code completion, vector embedding, and rerank models are for internal use by Costrict only and will not appear in the user-selectable model list.

### 3. Prepare Backend Service Images

Costrict backend images are mainly stored in the docker hub image repository docker.io/zgsm.

Before deployment, you need to ensure that the images required for backend deployment can be pulled from the image repository normally.

The images required by Costrict backend can be found in the scripts/newest-images.list file for a complete list.

You can get this list file from the cloud with the following command.

```bash
bash scripts/get-images-list.sh -o scripts
```

The deployment script will automatically pull all images required for backend deployment during the deployment process.

However, if the deployment server cannot access the docker hub image repository, you need to download the images in advance and save them to the specified directory of the deployment machine (assuming saved in /root/images). Then run the following command to preload them.

```bash
bash scripts/load-images.sh -l /root/images
```

In addition to pulling and exporting image files from the docker image repository, you can also download all image files required for Costrict backend deployment from Baidu Netdisk.

Netdisk address:

```
https://pan.baidu.com/s/12kP5VyQinFNrXFsKEWFGJw?pwd=k2dh
```

### 4. Service Deployment

Execute the automated deployment script:

```bash
bash deploy.sh
```

The deployment process includes the following steps:

1. Environment check and dependency verification
2. Docker image pulling and building
3. Database initialization
4. Service container startup
5. Health check and status verification

## Service Configuration

### AI Gateway Configuration (Higress)

After deployment, access the Higress console at the following address:

```
http://{COSTRICT_BACKEND}:{PORT_HIGRESS_CONTROL}
```

**Default admin username and password** (please change it after login):

```
Username: admin
Password: test123
```

Configuration steps:
1. Access the Higress management interface
2. Configure upstream LLM service providers
3. Set routing rules and load balancing strategies
4. Configure rate limiting and security policies

Detailed configuration guide: [Higress Configuration Document](./docs/higress.zh-CN.md)

### Identity Authentication System Configuration (Casdoor)

Access the Casdoor management interface at the following address:

```
http://{COSTRICT_BACKEND}:{PORT_CASDOOR}
```

**Test Account** (for development and testing environments only):
```
Username: demo
Password: test123
```

Configuration features:
- User management and permission control
- Third-party identity provider integration (OIDC/SAML)
- Multi-factor authentication (MFA)
- Session management and security policies

Detailed configuration guide: [Casdoor Configuration Document](./docs/casdoor.zh-CN.md)

## Client Integration

### VSCode Plugin Configuration

1. Install the Costrict VSCode extension
2. Open the "Provider" page in the extension settings
3. Select the API provider as "Costrict"
4. Configure the backend service address:
   ```
   Costrict Base URL: {COSTRICT_BACKEND_BASEURL}
   ```
5. Click "Login Costrict" to complete authentication

**Service Access Address**:
```
Default backend entry: http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}
```

### Domain Binding and Load Balancing

For production environments, it is recommended to access services through reverse proxy or load balancer:

```bash
# Nginx configuration example
upstream costrict_backend {
    server {COSTRICT_BACKEND}:{PORT_APISIX_ENTRY};
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://costrict_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Operations Management

### Service Status Monitoring

Check service running status:

```bash
# View all service status
docker-compose ps

# View service logs
docker-compose logs -f [service_name]

# View resource usage
docker stats
```

### Data Backup and Recovery

```bash
# Database backup
bash ./scripts/backup.sh

# Database recovery
bash ./scripts/restore.sh [backup_file]
```

### Service Scaling

```bash
# Scale service instances
docker-compose up -d --scale chatgpt=3

# Update service configuration
docker-compose up -d --force-recreate [service_name]
```

## Troubleshooting

### Common Issues

**1. Container startup failure**
```bash
# Check port occupancy
netstat -tlnp | grep {port}

# Check disk space
df -h

# View detailed error logs
docker-compose logs [service_name]
```

**2. Network connection issues**
```bash
# Test service connectivity
curl -v http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/health

# Check Docker network
docker network ls
docker network inspect {network_name}
```

**3. Database connection issues**
```bash
# Check database service status
docker-compose exec postgres pg_isready

# View database logs
docker-compose logs postgres
```

### Log Collection

System log locations:
- Application logs: `./logs/`
- Database logs: `/var/log/postgresql/` inside container
- Gateway logs: `/var/log/apisix/` inside container

## Security Notes

1. **Production Environment Deployment**:
   - Change all default passwords
   - Configure HTTPS certificates
   - Enable firewall and access control
   - Regularly update systems and dependencies

2. **Network Security**:
   - Only open necessary ports
   - Configure VPN or intranet access
   - Enable API rate limiting and protection

3. **Data Protection**:
   - Regularly backup important data
   - Enable database encryption
   - Configure access audit logs

## License

This project is open source under the Apache 2.0 license. See the [LICENSE](LICENSE) file for details.

## Support and Contribution

- **Issue Reporting**: [GitHub Issues](https://github.com/zgsm-ai/zgsm-backend-deploy/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/zgsm-ai/zgsm-backend-deploy/discussions)
- **Contribution Guidelines**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Costrict** - Let AI power your code development journey
