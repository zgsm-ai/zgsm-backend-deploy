# Deployment FAQ

This document records common issues and their solutions during the CoStrict backend service deployment process.

## 1. Backend Service Image Download Issues

### Issue1: How to download backend service images?

**Solution**:

Currently, two download methods are provided:
1. **Docker Hub**: If the deployment server can access Docker Hub, it is recommended to use this method directly.
2. **Baidu Cloud Drive**: If the deployment server cannot access Docker Hub, select a computer that can access Baidu Cloud Drive, download the images from Baidu Cloud Drive to the local machine, and then transfer them to the deployment server.

### Issue 2: Docker Hub image download timeout failure

**Solution**:

The failure may be caused by external network issues resulting in image access timeout. You can modify the image source to enable normal image download.

> Modify Docker image source
```bash
# Edit file: /etc/docker/daemon.json, add the following content
{
    "registry-mirrors": [
       "https://docker.m.daocloud.io",
       "https://docker.imgdb.de",
       "https://docker-0.unsee.tech",
       "https://docker.hlmirror.com",
       "https://cjie.eu.org"
    ]
}

# Restart docker service
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 2. ARM Architecture Machine Deployment Issues

### Issue: ARM architecture machine deployment failure

**Solution**:

The current private deployment project supports AMD architecture machine deployment. It is recommended to switch to an AMD architecture machine for deployment.

---

## 3. Docker Related Issues

### Issue: Docker command execution error when executing `deploy.sh` one-click deployment

**Solution**:

Check if the `docker` and `docker-compose` commands exist on the deployment server, and whether their versions are too low. Recommended versions:
- **Docker**: 20.10.24
- **Docker Compose**: v2.39.3

---

## 4. Port Occupancy Issues

### Issue: Port occupancy

**Solution**:

1. Connect to the backend deployment server and cd to the deployment project directory
2. Use the port check command from the deployment checklist to see which specific ports are occupied
3. Edit `configure.sh` with vi to change occupied ports to other unused ports, save `configure.sh`
4. Stop and delete containers related to the deployment project and clean up erroneous data
5. Re-execute the deploy.sh script for one-click deployment

> Port check command
```bash
sudo ss -tlnp | grep -E ':(39180|39080|32382|36379|35432|35003|39090|33000|39200|38001|39009) '
```

> Command to stop and delete containers related to the deployment project
```bash
# Method 1: Stop through docker-compose
docker-compose down

# Method 2: Stop through script
bash scripts/remove-containers.sh -f scripts/images.list
```

> Command to clean erroneous data
```bash
bash scripts/clean-storage.sh
```

---

## 5. User Login Related Issues

### Issue 1: Initial login account failure

**Solution**:

The CoStrict service deployed through the deployment project provides a default test account:
- **Username**: demo
- **Password**: test123

When logging in, please select the **"Password"** method to log in

### Issue 2: Account login shows client ID or secret error

**Cause**:
During deployment, due to system resources or performance issues, the initial record writing to postgres tables failed.

**Solution**:
1. Access `casdoor` page, click **"Identity Authentication"** to enter the application page
2. Select the **"Edit"** button in the **"Actions"** column of the record named **"loginApp"** to enter the edit page
3. Find the client configuration (`Client ID`, `Client Secret`) and modify it with the configuration in the `configure.sh` file in the deployment project directory (`OIDC_AUTH_CLIENT_ID`, `OIDC_AUTH_CLIENT_SECRET`)

**Note**: This method only handles the issue of missing client ID and secret configuration. Other missing initial records in postgres tables may cause other problems.

**Recommendation**:
> Method 1:

Use a server that meets deployment requirements to redeploy

> Method 2:

Connect to the current backend deployment server, cd to the deployment project directory, compare the SQL file content in `postgres/scripts` with the table records in the `postgres container` and supplement them

### Issue 3: Account login shows callback URL error

**Cause**:
During deployment, due to system resources or performance issues, the initial record writing to postgres tables failed.

**Solution**:

1. Access `casdoor` page, click **"Identity Authentication"** to enter the application page
2. Select the **"Edit"** button in the **"Actions"** column of the record named **"loginApp"** to enter the edit page
3. Find the redirect URLs configuration (`Redirect URLs`) and modify the content to: `http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/oidc-auth/api/v1/plugin/login/callback`

**Note**: This method only handles the issue of missing callback URL configuration. Other missing initial records in postgres tables may cause other problems.

**Recommendation**:
> Method 1:

Use a server that meets deployment requirements to redeploy

> Method 2:

Connect to the current backend deployment server, cd to the deployment project directory, compare the SQL file content in `postgres/scripts` with the table records in the `postgres container` and supplement them

### Issue 4: How to add new users

**Solution**:

1. Access `casdoor` page, click **"User Management"** to enter the organization page
2. Select the **"User"** button in the **"Actions"** column of the record named **"user-group"** to enter the user page of **"user-group"**
3. Click the **"Add"** button to add new users

### Issue 5: New user login failure

**Issue Details**:
```
code:oidc-auth.updateInfoFailed,data:"",message:"update user info fail:faile to create user:faile to create:ERROR: duplicate key value violate unique constraint \"idx_auth_users_github_id\"(SQLSTATE 23505)
```

**Solution**:

1. Connect to the backend deployment server and cd to the deployment project directory
2. Use `docker` command to connect to the `postgres` service container
3. After connecting to the `postgres` service, execute the following operations:
   - Switch db to auth: `\c auth;`
   - Drop the unique index: `drop index idx_auth_users_github_id;`
4. After completing the operations, use the new user to log in again in the `CoStrict` plugin

### Issue 6: User authentication expired

**Issue Details**:
```
API request failed
Error details:
Authentication expired
Authentication time: 11/3/2025, 11:32:55 AM
Expiration time: 11/10/2025, 11:32:55 AM
```

**Solution**:

Click the account avatar in the upper right corner of the CoStrict plugin to enter the account page, and click **"Relogin"** to log in.

### Issue 7: How to modify user authentication validity period

**Solution**:

1. Access the casdoor page, click **"Identity Authentication"** to enter the application page
2. Select the **"Edit"** button in the **"Actions"** column of the record named **"loginApp"** to enter the edit page
3. Find the authentication Token expiration configuration (`Access Token expiration`, `Refresh Token expiration`) and modify it

### Issue 8: Account interface webpage access error

**Issue Details**:

When clicking **"Buy More Quota"**, **"Participate in Activities to Get Quota"** and **"View Account Details"** on the account interface, the accessed webpages have errors.

**Solution**:

For private deployment, quota usage is not involved, so this can be ignored.

---

## 6. Model Update Issues

### Issue 1: Chat model updates

**Solution**:

1. Access `higress` page and check and configure the following three pages:
   - **AI Gateway Management -> AI Service Provider Management**: Configure model access information
   - **AI Gateway Management -> AI Route Management**: Configure model routing information
   - **Plugin Configuration -> AI Quota Management**: Configure optional model information for `CoStrict` plugin
2. After modification, click **Settings -> Provider** in the `CoStrict` plugin, then click **"Refresh Models"**

### Issue 2: Code Completion model updates

**Solution**:

1. Connect to the backend deployment server and cd to the deployment project directory
2. Edit `docker-compose.yml` with vi to modify the **code-completion** service configuration (`OPENAI_MODEL_HOST`, `OPENAI_MODEL`, `OPENAI_MODEL_AUTHORIZATION`)
3. Save `docker-compose.yml`
4. Stop and delete the **code-completion** service container
5. Restart the **code-completion** service container based on the updated `docker-compose.yml` file

> Stop and delete the **code-completion** service container
```bash
docker stop code-completion
docker rm code-completion
```

> Restart the **code-completion** service container based on the updated `docker-compose.yml` file
```bash
# Execute command in the deployment project directory
docker-compose up -d
```

### Issue 3: Embedding, Rerank model updates

**Solution**:

1. Connect to the backend deployment server and cd to the deployment project directory
2. Edit `codebase-embedder/conf.yaml` with vi to modify the **Embedder** and **Reranker** configurations under **VectorStore** (`Model`, `ApiKey`, `ApiBase`) respectively
3. Save `codebase-embedder/conf.yaml`
4. Stop and delete the **codebase-embedder** service container
5. Restart the **codebase-embedder** service container using the `docker-compose.yml` file based on the updated `codebase-embedder/conf.yaml` configuration file

> Stop and delete the **codebase-embedder** service container
```bash
docker stop codebase-embedder
docker rm codebase-embedder
```

> Restart the **codebase-embedder** service container using the `docker-compose.yml` file based on the updated `codebase-embedder/conf.yaml` configuration file
```bash
# Execute command in the deployment project directory
docker-compose up -d
```

### Issue 4: Conversation model updated in higress, but CoStrict plugin still shows old model list

**Cause Analysis 1**:

Possible failure to access backend service due to network or proxy issues

**Solution**:

Try accessing `http://{COSTRICT_BACKEND}:{PORT_APISIX_ENTRY}/ai-gateway/api/v1/models` in a browser to see if you can get the model list

**Cause Analysis 2**:

Due to configuration issues in `higress`, some plugins failed to start successfully, causing the configuration to not take effect

**Solution**:

1. Connect to the backend deployment server and enter the `higress` container using docker command
2. Navigate to the `/var/log/higress` directory and check the `gateway.log` content

### Issue 5: How to configure CoStrict to support image messages for newly added image-capable models

**Solution**:

1. First, ensure the model has image support capability
2. Access `higress` page, go to **Plugin Configuration -> AI Quota Management**
3. Click **"Configuration"** to enter the configuration page, select **"YAML View"** to display in yaml format, find the image-capable model configuration in the "providers" configuration item, and modify the "supportsImages" configuration to "true"
4. After modification, click **Settings -> Provider** in the CoStrict plugin, and click **"Refresh Models"**

---

## 7. Conversation Related Errors

### Issue 1: Conversation error

**Issue Details**:
```
API request failed
Error details:
zgsm completion error: Connection error
```

**Solution**:

The current error indicates: unable to access the deployed service server. There may be proxy-related issues on the local machine. It is recommended to check the local machine's proxy and other network issues.

### Issue 2: Simple conversations work, but conversation failure occurs after a few rounds

**Solution**:

The selected model may support a smaller context length. It is recommended to choose a model that supports **64k+** context.

---

## 8. Strict Mode Related Errors

### Issue: `Strict` mode generates files not in the specified directory

**Solution**:

`Strict` mode has higher requirements for model capabilities. The currently selected model may have insufficient instruction-following capabilities. It is recommended to choose **`glm-4.5` or higher** models.

---

## 9. Antivirus Software Related Warnings

### Issue: Computer antivirus software detects `codebase-indexer.exe` or `costrict.exe` as viruses

**Solution**:

These two services are client programs of the `CoStrict` plugin on the computer. It is recommended to modify the antivirus software to allow them to run.