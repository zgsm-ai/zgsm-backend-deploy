#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, TextField

logger = logging.getLogger(__name__)


class Conversation(BaseModel):
    """会话记录表"""

    class Meta:
        table_name = 'conversation'

    conversation_id = CharField(verbose_name='会话id')
    role = CharField(verbose_name='会话数据类型')
    content = TextField(verbose_name='会话内容')
    model = CharField(null=True, verbose_name='会话模型')

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
