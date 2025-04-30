#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from common.exception.exceptions import FieldValidateError
from common.helpers.response_helper import Result
from controllers.base import get_request_kwargs
from services.system.configuration_service import ConfigurationService

configuration = Blueprint('configuration', __name__)


@configuration.route('', methods=['GET'])
def get():
    """
    General configuration items
    Query: get api/configuration
        - Default type: Banner
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    search_kw = get_request_kwargs()
    if search_kw.get('belong_type', None) is None:
        raise FieldValidateError('[Type]: This input field cannot be empty')

    query, total = ConfigurationService.get_list(**search_kw)
    return Result.success(message='Get Success', data=query, total=total)


@configuration.route('/system', methods=['GET'])
def get_system_config():
    """
    Query system configuration items, such as IDE and web configurations
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    query = ConfigurationService.get_system_config()
    return Result.success(message='Get Success', data=query)
