#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/5/6 15:49
"""
from dao.base_dao import BaseDao
from models.system.api_rule import ApiRule


class ApiRuleDao(BaseDao):
    model = ApiRule
