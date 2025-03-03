# elasticsearch数据目录

```shell
chown -R 1000:1000 data
chmod -R 0664 data
```

需要把数据目录属组设置为1000，因为elasticsearch进程的属组为1000.
需要把数据目录权限设置为0664，保证elasticsearch可以在data下创建文件。

