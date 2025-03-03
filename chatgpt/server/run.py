#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
# import os
# sys.path.append(os.path.dirname(__file__))
# from __future__ import absolute_import

from app import create_app, conf
from common.constant import ServeConstant
from waitress import serve
import logging

# serve 并发配置
threads = int(conf.get("serve_threads", ServeConstant.THREADS))
connection_limit = int(conf.get("serve_connection_limit", ServeConstant.CONNECTION_LIMIT))
logging.warning(f"waitress.serve config threads: {threads}, connection_limit: {connection_limit}")
serve(create_app(), host="0.0.0.0", port="5000", threads=threads, connection_limit=connection_limit)
