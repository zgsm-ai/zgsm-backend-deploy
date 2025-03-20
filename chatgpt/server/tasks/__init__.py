#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/7/28 15:04
"""
import logging
from functools import wraps

import peewee
import psycopg2
from celery import Celery
from playhouse.db_url import connect

from config import CONFIG, conf
from db import db


def make_celery_app():
    celery = Celery('chatgpt_server')
    celery.config_from_object(CONFIG.celery)
    return celery


def handle_db(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            # pylint: disable=no-member
            if not db.obj:
                database = connect(conf.get('database_uri'))
                db.initialize(database)
            if db.obj.is_closed():
                db.obj.connect()
            return func(*args, **kwargs)

        except (psycopg2.InterfaceError, peewee.InterfaceError,
                psycopg2.OperationalError, peewee.OperationalError) as e:
            logging.error(f"error to connect the db: {e}, try to reconnect")
            # 如果在数据操作中出现了连接异常，可能会造成线程中的连接一直处于无效状态，所以需要先重置该连接，再捕获该异常。
            # If a connection exception occurs during data operations, the connection in the thread may remain invalid, so the connection needs to be reset first, and then the exception is caught.
            database = connect(CONFIG.app.DATABASE_URI)
            db.initialize(database)
            if db.obj.is_closed():
                db.obj.connect()
            raise e
        finally:
            # 使用了 poolext 的数据库连接，close 只是将使用完的连接放回 pool 中
            # Using a poolext database connection, close simply puts the completed connection back into the pool
            if not db.obj.is_closed():
                db.obj.close()

    return wrapped_func


celery_app = make_celery_app()

celery_app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': CONFIG.celery.celery_once.url,
        'default_timeout': CONFIG.celery.celery_once.timeout
    }
}

# 定时任务配置
# Scheduled task configuration
celery_app.conf.update(
    beat_schedule={
        'clean_up_expired_contexts_task': {
            'task': 'tasks.beat_task.clean_up_expired_contexts_task',
            'schedule': 24 * 60 * 60,
            'args': ()
        },
    }
)
