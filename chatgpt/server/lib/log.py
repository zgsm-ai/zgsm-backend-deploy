#!/usr/bin/env python
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
    Log filter that adds a sid field to each log record
    """
    def __init__(self, sid=None):
        super().__init__()
        self.sid = sid

    def filter(self, record):
        record.sid = self.sid
        return True

class SocketWrapper:
    """
    Add websocket sid to each log record in a context environment
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
