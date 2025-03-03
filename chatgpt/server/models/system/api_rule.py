#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/19 18:04
"""

from peewee import CharField

from common.constant import ApiRuleConstant
from models.base_model import BaseModel


class ApiRule(BaseModel):
    """api权限规则"""
    RULE_TYPE_CHOICES = ApiRuleConstant.RULE_TYPE_CHOICES

    class Meta:
        table_name = 'api_rule'

    rule_type = CharField(default='', choices=RULE_TYPE_CHOICES, verbose_name='类型')
    rule_info = CharField(default='', verbose_name='内容', help_text='部门：多级部门使用 “/” 隔开，例：研发体系/项目管理部<br>用户：姓名+工号')
