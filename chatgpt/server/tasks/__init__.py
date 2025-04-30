#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
            # If a connection exception occurs during database operations, it may cause the connection in the thread to remain in an invalid state, so we need to reset the connection first and then catch the exception.
            database = connect(CONFIG.app.DATABASE_URI)
            db.initialize(database)
            if db.obj.is_closed():
                db.obj.connect()
            raise e
        finally:
            # When using poolext database connection, close only puts the used connection back into the pool
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
