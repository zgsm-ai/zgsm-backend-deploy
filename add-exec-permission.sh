#!/bin/bash

# 脚本名称：add-exec-permission.sh
# 功能：为工作区下所有.sh文件、.sql文件和.sql.tpl文件添加运行权限

echo "开始为工作区下所有脚本文件添加运行权限..."

# 查找当前工作区及其子目录下的所有.sh文件，并添加执行权限
find . -type f -name "*.sh" -exec chmod +x {} \;
sh_count=$(find . -type f -name "*.sh" | wc -l)

# 查找当前工作区及其子目录下的所有.sql文件，并添加执行权限
find . -type f -name "*.sql" -exec chmod +x {} \;
sql_count=$(find . -type f -name "*.sql" | wc -l)

# 查找当前工作区及其子目录下的所有.sql.tpl文件，并添加执行权限
find . -type f -name "*.sql.tpl" -exec chmod +x {} \;
sql_tpl_count=$(find . -type f -name "*.sql.tpl" | wc -l)

# 计算总数
total_count=$((sh_count + sql_count + sql_tpl_count))

echo "已为以下文件添加运行权限："
echo "- $sh_count 个.sh文件"
echo "- $sql_count 个.sql文件"
echo "- $sql_tpl_count 个.sql.tpl文件"
echo "总计：$total_count 个文件"
echo "完成！"