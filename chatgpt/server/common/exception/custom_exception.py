#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/16 20:41
    :修改者: 苏德利 16646
    :更新时间: 2023/3/16 20:41
"""

import logging

logger = logging.getLogger(__name__)


class CustomException(Exception):
    msg = '错误'
    code = 500
    error_code = 160000
    send_to_sentry = True

    @classmethod
    def response(cls, error):
        logger.error(error, exc_info=True)
        if cls.send_to_sentry:
            try:
                from sentry_sdk import capture_exception
                capture_exception(error)
            except ImportError:
                pass
        from common.helpers.response_helper import Result
        return Result.fail(message=str(error), msg=str(error), code=cls.code)

    @classmethod
    def register(cls, app):
        app._register_error_handler(None, cls, cls.response)

    def __str__(self):
        return self.msg

    def __init__(self, msg=None):
        if msg:
            self.msg = msg
