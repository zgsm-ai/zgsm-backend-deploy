#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.api_rule import ApiRule


class ApiRuleDao(BaseDao):
    model = ApiRule
