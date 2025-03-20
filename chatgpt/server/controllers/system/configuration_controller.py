#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/20 10:55
"""

from flask import Blueprint

from common.exception.exceptions import FieldValidateError
from common.helpers.response_helper import Result
from controllers.base import get_request_kwargs
from services.system.configuration_service import ConfigurationService

configuration = Blueprint('configuration', __name__)


@configuration.route('', methods=['GET'])
def get():
    """
    Common configuration item
    Query: get api/configuration
        - Default type banner
    ---
    tags:
      - system
    responses:
      200:
        res: result
    """
    search_kw = get_request_kwargs()
    if search_kw.get('belong_type', None) is None:
        raise FieldValidateError('[Type] : This input item is not allowed to be empty')

    query, total = ConfigurationService.get_list(**search_kw)
    return Result.success(message='Obtained successfully', data=query, total=total)


@configuration.route('/system', methods=['GET'])
def get_system_config():
    """
    Query system configuration items, such as ide, web some configuration
    ---
    tags:
      - system
    responses:
      200:
        res: result
    """
    query = ConfigurationService.get_system_config()
    return Result.success(message='Obtained successfully', data=query)
