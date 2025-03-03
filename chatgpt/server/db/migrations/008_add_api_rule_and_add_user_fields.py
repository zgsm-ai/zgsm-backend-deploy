#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 11:05
"""

import peewee as pw

from models.system.api_rule import ApiRule
from models.system.users import Users

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    migrator.add_fields(Users, avatar_color=pw.CharField(default=''))
    migrator.create_model(ApiRule)


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    migrator.remove_fields(Users, 'avatar_color')
    migrator.remove_model(ApiRule)
