# 如何离线安装docker 和docker compose

## docker

### 下载docker包

下载地址[docker官网](https://download.docker.com/linux/static/stable/x86_64/),推荐下载版本[20.10.24](https://download.docker.com/linux/static/stable/x86_64/docker-20.10.24.tgz)

### 解压并转存

```bash
# docker-20.10.24.tgz 是文件下载的实际位置
tar -zxvf docker-20.10.24.tgz -C /tmp
cp /tmp/docker/* /usr/bin/
```


### 注册docker服务

vim /etc/systemd/system/docker.service

```
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target
[Service]
Type=notify
ExecStart=/usr/bin/dockerd --selinux-enabled=false --insecure-registry=127.0.0.1
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s
[Install]
WantedBy=multi-user.target
```


### 启动

```bash
chmod 777 /etc/systemd/system/docker.service
systemctl daemon-reload
systemctl enable docker
systemctl start docker
```


### 验证

```bash
systemctl status docker
docker -v
docker info
```

## docker compose

### 下载

下载地址 [github release](https://github.com/docker/compose/releases) 建议版本:[v2.39.3](https://github.com/docker/compose/releases/download/v2.39.3/docker-compose-linux-x86_64)

### 安装

```bash
# docker-compose-linux-x86_64 是文件下载的实际位置
sudo mv docker-compose-linux-x86_64 /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
cp -a /usr/local/bin/docker-compose  ~/.docker/cli-plugins/docker-compose # 添加到docker 子命令
```

### 验证

```bash
docker-compose 
docker compose
```