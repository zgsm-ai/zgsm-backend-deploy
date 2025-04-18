#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = None


def register_throttle(app):
    """Interface traffic limiting. No limit by default"""
    global limiter
    limiter = Limiter(
        app=app,
        storage_uri=os.environ.get('REDIS_URL'),
        key_prefix='flask-limiter',
        key_func=get_remote_address
    )
