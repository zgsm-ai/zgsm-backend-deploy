# postgres数据目录

```shell
chown -R 1000:1000 data
chmod -R 0775 data
```

需要把数据目录data属组设置为1000，因为postgres进程的属组为1000.
需要把数据目录data权限设置为0775，保证postgres可以在data下创建文件。

