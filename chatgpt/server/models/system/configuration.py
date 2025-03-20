#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/19 18:04
"""

from peewee import CharField, TextField

from models.base_model import BaseModel


class Configuration(BaseModel):
    """Generic configuration data model"""

    class Meta:
        table_name = 'configuration'

    belong_type = CharField(default='', verbose_name='Type')
    attribute_key = CharField(default='', verbose_name='Attribute Key')
    attribute_value = TextField(default='', verbose_name='Attribute Value',
                                help_text='Type banner: value is banner content'
                                          '<br>Type api_documentation: Please fill in markdown format'
                                          '<br>Type forbidden_word: Support regular expression')
    desc = CharField(default='', verbose_name='Description')
