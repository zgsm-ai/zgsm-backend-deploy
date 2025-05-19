# zgsm-backend-deploy Helm Chart

### Introduction

This Helm Chart helps you quickly deploy zgsm-backend services, including one-api, dex, fauxpilot, postgresql, redis, elasticsearch, apisix, and more.

### Before You Begin

- **Make sure to replace all placeholders like `<your domain>`, `<your oauth provider>` in `values.yaml` with your actual values.**
- **You must configure models in the one-api admin panel yourself.**
- **You also need to configure the completion model for fauxpilot (e.g., OPENAI_MODEL_HOST, OPENAI_MODEL) according to your needs.**

### Installation

```bash
helm install zgsm-backend kubernetes/helm -f kubernetes/helm/values.yaml --namespace shenma --create-namespace
```

### Key Configuration

#### 1. Domain & OAuth
In `values.yaml`, find and replace the following with your actual domain and OAuth provider info:

```yaml
dex:
  config:
    issuer: "http://<your domain>:5556/dex"
    staticClient:
      redirectURI: https://<your domain>/login/oidc
  connectors:
    redirectURI: "http://<your domain>:5556/dex/callback"
    tokenURL: https://<your oauth provider>/oauth2/token
    authorizationURL: https://<your oauth provider>/oauth2/authorize
    userInfoURL: https://<your oauth provider>/oauth2/get_user_info
    logoutURL: https://<your oauth provider>/oauth2/user_logout
```

#### 2. one-api Model Configuration
- After installing one-api, **log in to the one-api admin panel and manually add/configure the models** you need (e.g., OpenAI, Azure, DeepSeek, etc.).

#### 3. fauxpilot Completion Model Configuration
In the fauxpilot section of `values.yaml`:

```yaml
fauxpilot:
  env:
    OPENAI_MODEL_HOST: http://shenma-oneapi:3000/v1/completions
    OPENAI_MODEL: DeepSeek-Coder-V2-Lite-Base
    OPENAI_MODEL_API_KEY: "sk-xxxxxx"
```
- **Modify these according to your actual model service address and API Key.**

### Upgrade

```bash
helm upgrade zgsm-backend kubernetes/helm -f kubernetes/helm/values.yaml --namespace shenma
```

### Uninstall

```bash
helm uninstall zgsm-backend  --namspace shenma
```

### Other Notes
- Some default passwords/tokens are for demo only. Please change them in production.
- Adjust CPU/memory resource limits according to your environment.

### Support
If you have any questions, please submit an issue or contact the maintainer.

---

For further customization, please refer to the detailed comments in the `values.yaml` file. 