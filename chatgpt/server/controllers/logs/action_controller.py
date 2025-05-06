#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging

from flask import Blueprint, Response
from flask import request

from controllers.base import handle_validate
from services.action.complation_service import UserGiveFeedbacks
from common.helpers.application_context import ApplicationContext
from controllers.response_helper import Result

from third_platform.es.chat_messages.code_compeltion_es_service import code_completion_es_service
from third_platform.es.chat_messages.code_copy_es_service import code_copy_es_service
from third_platform.es.chat_messages.ide_data_as_service import ide_es_service
from third_platform.es.chat_messages.evaluate_es_service import evaluate_es
from third_platform.es.chat_messages.use_code_es_service import use_code_es
from third_platform.es.chat_messages.issue_es_service import issue_es

logs = Blueprint('logs', __name__)

def get_request_ide_data(data, user) -> dict:
    """
    Get data transmitted from IDE plugin
    """
    data['user_agent'] = request.headers.get("User-Agent")
    data['host'] = request.headers.get("Host")
    data['host_ip'] = request.headers.get("host-ip", "")
    data['ide'] = request.headers.get('ide', '')
    data['ide_version'] = request.headers.get('ide-version', '')
    data['ide_real_version'] = request.headers.get('ide-real-version', '')
    data["path"] = request.url or "/chat_agent"
    data['username'] = user.username
    data['display_name'] = user.display_name
    return data

#
#   Service key data recording
#   1. Completion:
#       1.1. API results
#

@logs.route("/completion", methods=['POST'])
def logs_completion():
    """
    Plugin-side feedback on code snippets accepted by users in code completion
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data = get_request_ide_data(data, user)

    code_completion_es_service.insert(data)
    return Result.success()
