#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tasks import celery_app, handle_db

@celery_app.task
@handle_db
def clean_up_expired_contexts_task():
    """
    Timed cleanup of expired session records
    """
    pass
