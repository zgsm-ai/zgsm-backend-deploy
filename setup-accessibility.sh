#!/bin/sh

chmod +x apisix-chatgpt.sh
chmod +x apisix-copilot.sh
chmod +x apisix-keycloak.sh
chmod +x configure.sh
chmod +x tpl-resolve.sh

chown -R 1000:1000 etcd/data
chown -R 1000:1000 es/data
chmod -R 0775 es/data