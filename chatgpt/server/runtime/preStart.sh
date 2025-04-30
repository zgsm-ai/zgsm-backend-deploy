#!/bin/sh
# This script is used to start workers stopped by the preStop.sh script when the pod starts

host_name=$(hostname)
# Cannot use active_queues when starting
celery_group_list=$(cat /server/runtime/supervisord-celery.conf |grep 'queues=' |awk -F 'queues=' '{print $2}' |awk '{print $1}')
# Add default celery
celery_group_list="celery ${celery_group_list}"

# Start worker consumption
for celery_group in ${celery_group_list};
do
  echo "[${host_name}][`date`] add celery worker ${celery_group}"
  celery -A tasks control add_consumer ${celery_group} -d celery@${host_name}
  # Use add_consumer when starting
done
