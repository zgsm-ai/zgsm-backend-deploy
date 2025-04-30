#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import peewee as pw

from common.constant import UserConstant
from services.system.users_service import UsersService

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    # Update existing users' avatar background color
    users, _ = UsersService.list(deleted=None)
    for user in users:
        avatar_color = random.choice(UserConstant.AVATAR_COLORS)
        user.avatar_color = avatar_color
        user.save()


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    pass
