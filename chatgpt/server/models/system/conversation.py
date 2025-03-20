#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, TextField

logger = logging.getLogger(__name__)


class Conversation(BaseModel):
    """Conversation record table"""

    class Meta:
        table_name = 'conversation'

    conversation_id = CharField(verbose_name='Conversation id')
    role = CharField(verbose_name='Conversation data type')
    content = TextField(verbose_name='Conversation content')
    model = CharField(null=True, verbose_name='Conversation model')

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
