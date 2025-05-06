#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import CharField, TextField, IntegerField

from db.custom_field import JSONField
from models.base_model import BaseModel


class PromptSquare(BaseModel):
    """Prompt Square"""

    title = CharField(default='', index=True, verbose_name='Title')
    prompt = TextField(default='', verbose_name='Question')
    prompt_completion = JSONField(default=[], verbose_name='Q&A')
    hot = IntegerField(default=0, verbose_name='Popularity/Citation Count')
    creator = CharField(default='', index=True, verbose_name='Creator')

    class Meta:
        table_name = 'prompt_square'

    def __str__(self):
        return self.title
