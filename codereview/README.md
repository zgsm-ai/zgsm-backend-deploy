# codereview

codereview包括三个镜像，4个服务，review-manager、review-worker这两个服务使用相同镜像。

## 资源配置

### review-manager

image: szondocker.sangfor.com/prod-docker/review-manager:1.0.18
cpu：20m  内存：200M  磁盘：1G

### review-worker

image: szondocker.sangfor.com/prod-docker/review-manager:1.0.18
cpu：20m  内存：200M  磁盘：1G

### review-checker

image: szondocker.sangfor.com/prod-docker/review-checker:1.0.11
cpu：20m  内存：200M  磁盘：1G

### issue-manager

image: szondocker.sangfor.com/prod-docker/issue-manager:1.0.8
cpu：10m  内存：200M  磁盘：1G

### 数据库

地址：postgres:5432
数据库名：codereview
表名：engine、issues、review_task

### redis

地址：redis:6379
库：0、2
缓存前缀:

- review_task:status:
- asynq:{critical}:
- asynq:{default}:
- prompt_template:list:
