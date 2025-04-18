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

feedbacks = Blueprint('feedbacks', __name__)

def get_request_ide_data(data, user) -> dict:
    """
    Get the data transmitted by the IDE plugin
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
#   User feedback:
#   1. Completion:
#       1.1. Accept the completion content
#       1.2. Performance statistics of completion results
#       1.3. Client error
#   2. Dialogue/Generation
#       2.1. Evaluation
#       2.2. Accept code, copy code
#       2.3. Performance statistics
#       2.4. Client error
#

@feedbacks.route("/completion", methods=['POST'])
def feedback_completion():
    """
    The plug-in end feeds back the code snippets accepted by the user in code completion
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data = get_request_ide_data(data, user)

    code_completion_es_service.insert(data)
    return Result.success()

@feedbacks.route('/completions', methods=['POST'])
def feedback_completions():
    """
    The plug-in end feeds back a set of completion results
    """

    return Result.success()

@feedbacks.route("/copy_code", methods=['POST'])
def feedback_copy_code():
    """
    Feedback that the user copied the code during the AI dialogue process
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data = get_request_ide_data(data, user)

    code_copy_es_service.insert_code_completion(data)

    return Result.success()

@feedbacks.route('/evaluate', methods=['POST'])
@handle_validate(UserGiveFeedbacks)
def feedback_evaluate(fields):
    """
    Feedback evaluation: like or dislike
    """
    try:
      logging.info("feedback_evaluate: ", fields, request.headers)

      conv_id = fields.get("conversation_id")
      user = ApplicationContext.get_current()
      fields = get_request_ide_data(fields, user)

      evaluate_es.insert(fields, id=conv_id)
      return Response(json.dumps({"status": "ok"}), status=200, mimetype='application/json', headers={
          "Content-Type": "application/json",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
      })
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json', headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })

@feedbacks.route('/use_code', methods=['POST'])
def feedback_use_code():
    """
    User feedback uses code through operations such as ctrlc,copy,accept,diff
    """
    try:
        status = 200
        request_data = request.get_json()
        logging.info("feedback_use_code: ", request_data, request.headers)
        if not request_data:
            res, status = {"error": "Invalid input: JSON data is required"}, 403
        conv_id = request_data.get("conversation_id")
        accept_num = request_data.get("accept_num") or 0
        # Add user interaction behavior, compatible with the old version, no field verification
        behavior = request_data.get("behavior", "")
        if not conv_id or not isinstance(conv_id, str):
            res, status = {"error": "Invalid input: 'conversation_id' must be a non-empty string"}, 403
        if not isinstance(accept_num, int):
            res, status = {"error": "Invalid input: 'accept_num' must be an integer"}, 403
        if not isinstance(behavior, str):
            res, status = {"error": "Invalid input: 'behavior' must be a string"}, 403

        use_code_es.insert(request_data, id=conv_id)
        res, status = {"status": "ok"}, 200
        return Response(json.dumps(res), status=status, mimetype='application/json', headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json', headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })

@feedbacks.route('/issue', methods=['POST'])
def feedback_issue():
    """
    Feedback question: problem description, problem type, screenshot, contact phone number
    """
    user = ApplicationContext.get_current()
    data = request.get_json()
    data = get_request_ide_data(data, user)

    issue_es.insert_issue(data)

    return Result.success()
