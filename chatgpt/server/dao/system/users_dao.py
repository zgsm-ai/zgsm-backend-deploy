#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    simple introduction

    :Author: Sudeli 16646
    :Time: 2023/3/14 15:51
    :Modifier: Sudeli 16646
    :UpdateTime: 2023/3/14 15:51
"""

from dao.base_dao import BaseDao
from models.system.users import Users


class UsersDao(BaseDao):
    model = Users
