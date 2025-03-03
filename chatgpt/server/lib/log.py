#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    设置log debug模式是否开启

    :作者: 苏德利 16646
    :时间: 2023/3/29 10:01
    :修改者: 苏德利 16646
    :更新时间: 2023/3/29 10:01
"""
# -*- coding: utf-8 -*-
from logging import Filter, Formatter, Logger
from config import conf
from contextlib import contextmanager


class RequireDebugFalse(Filter):
    def filter(self, record):
        return not conf.get('log_debug')


class RequireDebugTrue(Filter):
    def filter(self, record):
        return conf.get('log_debug')

class SocketFilter(Filter):
    """
    日志过滤器，该过滤器给每条日志记录加上一个sid字段
    """
    def __init__(self, sid=None):
        super().__init__()
        self.sid = sid

    def filter(self, record):
        record.sid = self.sid
        return True

class SocketWrapper:
    """
    给某个上下文环境下的每条日志记录加上websocket的sid
    """
    @staticmethod
    @contextmanager
    def with_sid(logger: Logger, sid: str):
        sid_filter = SocketFilter(sid)
        logger.addFilter(sid_filter)

        try:
            yield
        finally:
            logger.removeFilter(sid_filter)
