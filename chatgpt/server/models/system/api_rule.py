#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import CharField

from common.constant import ApiRuleConstant
from models.base_model import BaseModel


class ApiRule(BaseModel):
    """API permission rules"""
    RULE_TYPE_CHOICES = ApiRuleConstant.RULE_TYPE_CHOICES

    class Meta:
        table_name = 'api_rule'

    rule_type = CharField(default='', choices=RULE_TYPE_CHOICES, verbose_name='Type')
    rule_info = CharField(default='', verbose_name='Content', help_text='Department: multi-level departments use "/" to separate, e.g.: R&D System/Project Management Dept<br>User: Name+Employee ID')
