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
    通用配置项
    查询: get api/configuration
        - 默认类型 横幅
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    search_kw = get_request_kwargs()
    if search_kw.get('belong_type', None) is None:
        raise FieldValidateError('[类型] ：该输入项不允许为空')

    query, total = ConfigurationService.get_list(**search_kw)
    return Result.success(message='获取成功', data=query, total=total)


@configuration.route('/system', methods=['GET'])
def get_system_config():
    """
    查询系统配置项，比如ide、web一些配置
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    query = ConfigurationService.get_system_config()
    return Result.success(message='获取成功', data=query)
