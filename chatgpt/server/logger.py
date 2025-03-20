#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Registration log processing module

    :Author: Su Deli 16646
    :Time: 2023/3/29 9:47
    :Modifier: Su Deli 16646
    :UpdateTime: 2023/3/29 9:47
"""
import os
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import logging.config
import yaml
from common.constant import LoggerNameContant

runtime_path = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(runtime_path, 'logs')


def setup_logging(default_path='config/logging.yml',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging configuration
    :param default_path:
    :param default_level:
    :param env_key:
    :return:
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        config = yaml.safe_load(open(path))
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    # Hide useless log printing of non-3rd party packages
    pydantic_spec_logger = logging.getLogger('flask_pydantic_spec.config')
    pydantic_spec_logger.setLevel(logging.ERROR)

def gen_handler(level, name):
    filename = os.path.join(log_dir, f'{name}.log')

    # 500M
    handler = RotatingFileHandler(
        filename, maxBytes=524288000, backupCount=5, encoding='utf8')
    handler.setLevel(level)
    handler.setFormatter(Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    return handler


def register_logger(app):
    setup_logging()
    error_handler = gen_handler('ERROR', 'error')
    info_handler = gen_handler('INFO', 'info')

    app.logger.addHandler(error_handler)
    app.logger.addHandler(info_handler)


task_chat_logger = None
def get_task_chat_logger():
    """
    Calling openai.chat.completions API is an asynchronous operation, and the log of this operation process is recorded by the logger returned by this function
    """
    global task_chat_logger
    if task_chat_logger is not None:
        return task_chat_logger
    error_handler = gen_handler('ERROR', 'task_chat_error')
    info_handler = gen_handler('INFO', 'task_chat_info')
    task_chat_logger = logging.getLogger("task_chat")
    task_chat_logger.setLevel(logging.DEBUG)
    task_chat_logger.addHandler(error_handler)
    task_chat_logger.addHandler(info_handler)
    # Set the formatter for all handlers
    formatter = Formatter('%(asctime)s - %(levelname)s - [SID: %(sid)s] - %(message)s')
    for handler in task_chat_logger.handlers:
        handler.setFormatter(formatter)
    return task_chat_logger

socket_server_logger = None
def get_socket_server_logger():
    global socket_server_logger
    if socket_server_logger is not None:
        return socket_server_logger
    error_handler = gen_handler('ERROR', 'socket_server_error')
    info_handler = gen_handler('INFO', 'socket_server_info')
    socket_server_logger = logging.getLogger(LoggerNameContant.SOCKET_SERVER)
    socket_server_logger.setLevel(logging.INFO)
    socket_server_logger.addHandler(error_handler)
    socket_server_logger.addHandler(info_handler)
    return socket_server_logger


sio_logger = None
def get_sio_logger():
    global sio_logger
    if sio_logger is not None:
        return sio_logger
    sio_info_handler = gen_handler('INFO', 'sio_info')
    sio_logger = logging.getLogger(LoggerNameContant.SIO)
    sio_logger.setLevel(logging.INFO)
    sio_logger.addHandler(sio_info_handler)
    return sio_logger
