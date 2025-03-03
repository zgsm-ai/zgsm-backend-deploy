#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/5/9 11:59
"""
from peewee import fn

from common.constant import ApiRuleConstant
from dao.system.api_rule_dao import ApiRuleDao
from services.base_service import BaseService


class ApiRuleService(BaseService):
    dao = ApiRuleDao

    @classmethod
    def user_rule_is_exist(cls, display_name):
        if cls.dao.get_nums(rule_type=ApiRuleConstant.USER, rule_info=display_name) > 0:
            return True
        return False

    @classmethod
    def dept_rule_is_exist(cls, department):
        fields = {
            'rule_type': ApiRuleConstant.DEPT,
            'conditions': ((ApiRuleService.dao.model.rule_info != '')
                           & (fn.CONCAT(department, '%').contains(ApiRuleService.dao.model.rule_info)),)
        }
        if cls.dao.get_nums(**fields) > 0:
            return True
        return False

    @classmethod
    def rule_is_exist(cls, mid, rule_type, rule_info):
        fields = {
            'conditions': ((ApiRuleService.dao.model.id != mid),),
            'rule_type': rule_type,
            'rule_info': rule_info,
            'deleted': False
        }
        if cls.dao.get_nums(**fields) > 0:
            return True
        return False
