#!/bin/sh
# 该脚本用于pod启动执行preStop.sh脚本停止的worker

host_name=$(hostname)
# 启动的时候不能使用active_queues获取
celery_group_list=$(cat /server/runtime/supervisord-celery.conf |grep 'queues=' |awk -F 'queues=' '{print $2}' |awk '{print $1}')
# 添加默认的celery
celery_group_list="celery ${celery_group_list}"

# 启动worker消费
for celery_group in ${celery_group_list};
do
  echo "[${host_name}][`date`] add celery worker ${celery_group}"
  celery -A tasks control add_consumer ${celery_group} -d celery@${host_name}
  # 启动是add_consumer
done
