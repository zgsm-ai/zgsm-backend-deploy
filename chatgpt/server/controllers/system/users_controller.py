#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 14:09
"""

from flask import Blueprint, request

from common.helpers.application_context import ApplicationContext
from common.helpers.response_helper import Result
from services.system.users_service import users_service
from third_platform.es.chat_messages.code_compeltion_es_service import code_completion_es_service
from third_platform.es.chat_messages.code_copy_es_service import code_copy_es_service
from third_platform.es.chat_messages.prompt_es_service import prompt_es_service

users = Blueprint('users', __name__)


@users.route('/current', methods=['GET'])
def current():
    """
    当前用户
    ---
    tags:
      - 用户管理
    responses:
      200:
        res: 结果
    """
    user = ApplicationContext.get_current()
    return Result.success(message='获取成功', data=user)


@users.route("/key", methods=["GET", "POST"])
def generate_api_key():
    """
    用于获取或重置api key
    ---
    tags:
      - 用户管理
    responses:
      200:
        res: 结果
    """
    user = ApplicationContext.get_current()
    if request.method == "POST":
        user = users_service.update_api_key(user)
    return Result.success(message='获取成功', data=user)


@users.route("/code_completion_log", methods=['POST'])
def code_completion_log():
    """
    用于记录 用户在使用 千流ai插件中代码补全 或 生成代码的上报数据。
    ---
    tags:
      - 用户管理
    responses:
      200:
        res: 结果
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data['username'] = user.username
    data['display_name'] = user.display_name
    data['ide'] = request.headers.get('ide', '')
    data['ide_version'] = request.headers.get('ide-version', '')
    data['ide_real_version'] = request.headers.get('ide-real-version', '')
    accept_key = "isAccept"
    if accept_key in data.keys():
        # 部分场景需要统计用户接收度，如tp的用例优化和ide的划词对话产场景
        prompt_es_service.insert_prompt(data)
    else:
        code_completion_es_service.insert_code_completion(data)
    return Result.success()


@users.route("/code_copy_log", methods=['POST'])
def code_copy_log():
    """
    用于记录 用户在使用 千流ai插件 或者 web 端中 复制代码的上报数据。
    ---
    tags:
      - 用户管理
    responses:
      200:
        res: 结果
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data['display_name'] = user.display_name
    data['ide'] = request.headers.get('ide', '')
    data['ide_version'] = request.headers.get('ide-version', '')
    data['ide_real_version'] = request.headers.get('ide-real-version', '')

    code_copy_es_service.insert_code_completion(data)

    return Result.success()

