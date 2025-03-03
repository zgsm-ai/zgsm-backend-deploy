#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 09:21
"""
from peewee import CharField, TextField, IntegerField

from db.custom_field import JSONField
from models.base_model import BaseModel


class PromptSquare(BaseModel):
    """prompt广场"""

    title = CharField(default='', index=True, verbose_name='标题')
    prompt = TextField(default='', verbose_name='问题')
    prompt_completion = JSONField(default=[], verbose_name='问答')
    hot = IntegerField(default=0, verbose_name='热度/引用量')
    creator = CharField(default='', index=True, verbose_name='创建人')

    class Meta:
        table_name = 'prompt_square'

    def __str__(self):
        return self.title
