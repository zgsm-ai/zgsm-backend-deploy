#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.users import Users


class UsersDao(BaseDao):
    model = Users
