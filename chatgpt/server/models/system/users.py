#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import CharField, TextField, BooleanField
from models.base_model import BaseModel


class Users(BaseModel):
    """users information"""

    class Meta:
        table_name = 'users'

    username = CharField(null=True, verbose_name='User Account')
    display_name = CharField(null=True, verbose_name='User Display Name', help_text='Name + Account')
    email = CharField(null=True, verbose_name='Email')
    avatar_color = CharField(default='', verbose_name='Avatar Background Color')
    api_key = TextField(null=True, verbose_name='api_key')
    is_admin = BooleanField(default=False, verbose_name='Is Administrator')
    is_plus = BooleanField(default=False, verbose_name='Is Plus Permission')
    description = TextField(null=True, verbose_name='Description')

    def __str__(self):
        return self.display_name
