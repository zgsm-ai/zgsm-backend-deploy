#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 15:51
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 15:51
"""

from dao.base_dao import BaseDao
from models.system.users import Users


class UsersDao(BaseDao):
    model = Users
