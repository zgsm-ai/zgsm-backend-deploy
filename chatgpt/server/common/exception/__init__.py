#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Sudeli 16646
    :Time: 2023/3/14 15:41
    :Modifier: Sudeli 16646
    :UpdateTime: 2023/3/14 15:41
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
        # Basicly url 404
        return Result.fail(message="Request exception, please check if the url is correct", debug_info=error.description, code=error.code)
    return Result.fail(message="Service or network exception", debug_info=str(error), code=500)


def register_exception(app):
    is_debug = app.config.get("DEBUG", False)
    is_test = app.config.get('TESTING', False)
    capture_error = os.getenv('CAPTURE_ERROR')
    # Only the production environment registers or specifies environment variables
    if (not is_debug and not is_test) or capture_error:
        app.register_error_handler(Exception, error_handler)

    for exception in EXCEPTIONS:
        exception.register(app)
