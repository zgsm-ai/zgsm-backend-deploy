#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/19 18:04
"""

from peewee import CharField, TextField

from models.base_model import BaseModel


class Configuration(BaseModel):
    """通用的配置数据模型"""

    class Meta:
        table_name = 'configuration'

    belong_type = CharField(default='', verbose_name='类型')
    attribute_key = CharField(default='', verbose_name='属性键')
    attribute_value = TextField(default='', verbose_name='属性值',
                                help_text='类型 banner：值为横幅内容'
                                          '<br>类型 api_documentation：请填入markdown格式'
                                          '<br>类型 forbidden_word：支持正则')
    desc = CharField(default='', verbose_name='描述')
