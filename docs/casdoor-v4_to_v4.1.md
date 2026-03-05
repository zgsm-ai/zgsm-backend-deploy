# v4 casdoor to v4.1

注意，这是v4版本部署后，想要使用新版本casdoor的 **有损** 升级教程，而不是从0开始部署的教程，升级前，请自行下载 zgsm/casdoor:v2.0.10 镜像的tar包并导入到docker。

升级后请不要再执行v4版本的deploy.sh,否则sql脚本的运行，可能导致异常

## 关停服务

关停casdoor和oicd-auth(oidc也会连接到casdoor数据库,所以需要先停止)

请到部署目录执行

```bash
docker compose down oidc-auth casdoor
```

## 修改数据库

<font color='red'>警告,这将会导致casdoor 数据清空</font>

<font color='red'>警告,这将会导致casdoor 数据清空</font>

<font color='red'>警告,这将会导致casdoor 数据清空</font>

> 请手动复制命令，一条条执行;请手动复制命令，一条条执行

```bash
docker compose exec -it postgres /bin/bash # 注意，运行此命令后，你将进入容器。

# 登录到数据库
psql -h localhost -p 5432 -U zgsm # 注意，运行此命令后，将连接到数据库

# 删除数据库,再次警告，这将清空casdoor数据
DROP DATABASE IF EXISTS casdoor;
# 创建数据库
CREATE DATABASE casdoor;

# 退出数据库连接
\q
# 退出容器
exit

```

## 修改compose文件

到部署目录下，修改docker-compose.yaml

```bash
vim docker-compose.yml
```

找到：
```yaml
  casdoor:
    image: zgsm/casdoor:v2.0.10
    restart: always
    ports:
      - "39009:8000"
```

修改image为`zgsm/casdoor:v2.0.10`

## 启动服务

```bash
docker compose up -d oidc-auth casdoor
```

## 配置casdoor 

参考 [v4.1 casdoor配置](./casdoor-v4.1-use.md)