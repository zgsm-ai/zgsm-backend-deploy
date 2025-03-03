#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 15:41
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 15:41
"""
import os

from flask import current_app
from werkzeug.exceptions import HTTPException

from controllers.response_helper import Result
from .exceptions import EXCEPTIONS


def error_handler(error):
    # log
    current_app.logger.error(error, exc_info=True)
    # sentry
    try:
        from sentry_sdk import capture_exception
        capture_exception(error)
    except ImportError:
        pass
    if type(error) in EXCEPTIONS:
        message = str(error)
        return Result.fail(message=message, code=500)
    elif isinstance(error, HTTPException):
        # 基本就是 url 404
        return Result.fail(message="请求异常，请检查 url 是否正确", debug_info=error.description, code=error.code)
    return Result.fail(message="服务或网络异常", debug_info=str(error), code=500)


def register_exception(app):
    is_debug = app.config.get("DEBUG", False)
    is_test = app.config.get('TESTING', False)
    capture_error = os.getenv('CAPTURE_ERROR')
    # 只有生产环境才注册或指定环境变量
    if (not is_debug and not is_test) or capture_error:
        app.register_error_handler(Exception, error_handler)

    for exception in EXCEPTIONS:
        exception.register(app)
