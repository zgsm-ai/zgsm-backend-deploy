#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, TextField

logger = logging.getLogger(__name__)


class Conversation(BaseModel):
    """Conversation Records Table"""

    class Meta:
        table_name = 'conversation'

    conversation_id = CharField(verbose_name='Conversation ID')
    role = CharField(verbose_name='Conversation Data Type')
    content = TextField(verbose_name='Conversation Content')
    model = CharField(null=True, verbose_name='Conversation Model')

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
