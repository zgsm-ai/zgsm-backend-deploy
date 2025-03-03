#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    user列表

    :作者: 苏德利 16646
    :时间: 2023/3/14 14:14
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 14:14
"""

from peewee import CharField, TextField, BooleanField
from models.base_model import BaseModel


class Users(BaseModel):
    """users 信息"""

    class Meta:
        table_name = 'users'

    username = CharField(null=True, verbose_name='用户帐号')
    display_name = CharField(null=True, verbose_name='用户显示名', help_text='姓名+账号')
    email = CharField(null=True, verbose_name='邮箱')
    avatar_color = CharField(default='', verbose_name='头像背景色')
    api_key = TextField(null=True, verbose_name='api_key')
    is_admin = BooleanField(default=False, verbose_name='是否管理员')
    is_plus = BooleanField(default=False, verbose_name='是否plus权限')
    description = TextField(null=True, verbose_name='描述')

    def __str__(self):
        return self.display_name
