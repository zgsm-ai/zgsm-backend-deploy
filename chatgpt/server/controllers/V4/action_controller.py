#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Blueprint, Response
from flask import request

from controllers.base import handle_validate
from services.action.complation_service import UserGiveFeedbacks
from services.system.configuration_service import ConfigurationService
from common.helpers.application_context import ApplicationContext
from third_platform.es.chat_messages.ide_data_as_service import ide_es_service

actions_v4 = Blueprint('actions_v4', __name__)

@actions_v4.route('/give_like', methods=['POST'])
@handle_validate(UserGiveFeedbacks)
def give_like(fields):
    """
    User like interface, processes both Dify and ES platforms
    Note: Quick commands don't have like functionality, therefore no message_id
    ---
    tags:
      - Completion
    responses:
      200:
        result: Stream

    """
    conv_id = fields.pop("conversation_id")
    name = fields.pop("agent_name")
    user = ApplicationContext.get_current()
    if user:
        fields["user"] = user.display_name

    res, status = ide_es_service.user_evaluate(name, conv_id, **fields)
    return Response(json.dumps(res), status=status, mimetype='application/json', headers={
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    })


@actions_v4.route('/user_feedbacks', methods=['POST'])
def user_feedbacks():
    """
    User feedback
    ---
    tags:
      - Completion
    responses:
      200:
        res: Result

    """
    try:
        status = 200
        request_data = request.get_json()
        if not request_data:
            res, status = {"error": "Invalid input: JSON data is required"}, 403
        conv_id = request_data.get("conversation_id")
        accept_num = request_data.get("accept_num") or 0
        # Add user interaction behavior, compatible with older versions, no field validation
        behavior = request_data.get("behavior", "")
        if not conv_id or not isinstance(conv_id, str):
            res, status = {"error": "Invalid input: 'conversation_id' must be a non-empty string"}, 403
        if not isinstance(accept_num, int):
            res, status = {"error": "Invalid input: 'accept_num' must be an integer"}, 403

        res = ide_es_service.user_behavior(conv_id, accept_num, request_data)
        return Response(json.dumps(res), status=status, mimetype='application/json', headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })
    except Exception as e:
        return Response(json.dumps({"error": {e}}), status=500, mimetype='application/json', headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })

