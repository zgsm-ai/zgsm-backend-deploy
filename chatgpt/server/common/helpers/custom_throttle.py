#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/21 10:53
"""
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = None


def register_throttle(app):
    """接口限流。默认不限"""
    global limiter
    limiter = Limiter(
        app=app,
        storage_uri=os.environ.get('REDIS_URL'),
        key_prefix='flask-limiter',
        key_func=get_remote_address
    )
