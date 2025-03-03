#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/8/9 17:04
"""
from tasks import celery_app, handle_db

@celery_app.task
@handle_db
def clean_up_expired_contexts_task():
    """
    定时清理过期会话记录
    """
    pass
