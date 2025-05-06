#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
    Current user
    ---
    tags:
      - User Management
    responses:
      200:
        res: Result
    """
    user = ApplicationContext.get_current()
    return Result.success(message='Get Success', data=user)


@users.route("/key", methods=["GET", "POST"])
def generate_api_key():
    """
    Used to get or reset API key
    ---
    tags:
      - User Management
    responses:
      200:
        res: Result
    """
    user = ApplicationContext.get_current()
    if request.method == "POST":
        user = users_service.update_api_key(user)
    return Result.success(message='Get Success', data=user)


@users.route("/code_completion_log", methods=['POST'])
def code_completion_log():
    """
    For recording user data when using code completion or generating code in Qianliu AI plugin.
    ---
    tags:
      - User Management
    responses:
      200:
        res: Result
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
        # Some scenarios need to track user acceptance rate, such as TP's use case optimization and IDE's text selection dialog scenarios
        prompt_es_service.insert_prompt(data)
    else:
        code_completion_es_service.insert_code_completion(data)
    return Result.success()


@users.route("/code_copy_log", methods=['POST'])
def code_copy_log():
    """
    For recording user data when copying code in Qianliu AI plugin or web interface.
    ---
    tags:
      - User Management
    responses:
      200:
        res: Result
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data['display_name'] = user.display_name
    data['ide'] = request.headers.get('ide', '')
    data['ide_version'] = request.headers.get('ide-version', '')
    data['ide_real_version'] = request.headers.get('ide-real-version', '')

    code_copy_es_service.insert_code_completion(data)

    return Result.success()

