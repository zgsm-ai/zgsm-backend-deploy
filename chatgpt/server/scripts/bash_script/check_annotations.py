#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 15:18
# @Author  : 苏德利16646
# @Contact : 16646@sangfor.com
# @File    : check_annotations.py
# @Software: PyCharm
# @Project : chatgpt-server
# @Desc    : 用于检查AF自动化关键字规范https://ipd.atrust.sangfor.com/ipd/team/3580/issue/905355

import os
import re
import pandas as pd
import sys

# 定义列表数据
data = []


def check_keyword_annotations(file_path):
    check_status_list = [True, ]
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配 @keyword() 装饰器及其后面的注释
    keyword_pattern = re.compile(r'@keyword\(\)\s*def\s+(\w+)\(.*?\):\s*"""(.*?)"""', re.DOTALL)
    matches = keyword_pattern.findall(content)

    for (function_name, match) in matches:
        if '@name' not in match or '@desc' not in match or '@params' not in match or '@expect' not in match:
            print(f"File {file_path} is missing @name or @desc or @params or @expect in @keyword() annotation.")
            print(f"Match function_name: {function_name}")
            check_status = False
        else:
            check_status = True
        check_status_list.append(check_status)
        data.append([file_path, function_name, check_status])
    return check_status_list


def check_directory(directory):
    all_files_checked = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not check_keyword_annotations(file_path):
                    print(f"File {file_path} is missing @name or @desc in @keyword() annotation.")
                    all_files_checked = False
    return all_files_checked


def save_to_excel(form_data):
    # 定义表头信息
    columns = ["filename", "keyword", "check_status"]

    # 创建DataFrame
    df = pd.DataFrame(form_data, columns=columns)

    # 或者保存到CSV文件
    df.to_csv("output.csv", index=False)

    print("数据已成功保存到表格中。")


if __name__ == "__main__":
    directory_to_check = './keywords/utils/system_management/'  # 替换为你要检查的目录路径
    directory_to_check = sys.argv[1]
    if not os.path.exists(directory_to_check):
        print(f"Directory {directory_to_check} does not exist.")
        exit(1)
    if check_directory(directory_to_check):
        print("All files contain @name and @desc in @keyword() annotations.")
    else:
        print("Some files are missing @name or @desc in @keyword() annotations.")
    save_to_excel(data)
