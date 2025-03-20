#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/5/6 16:04
"""
import logging

from flask_admin.contrib.peewee.filters import BasePeeweeFilter
from wtforms import ValidationError

from admin.auth import AdminPermission
from admin.base import BaseView
from models.system.api_rule import ApiRule
from services.system.api_rule_service import ApiRuleService

logger = logging.getLogger(__name__)

class CustomFilter(BasePeeweeFilter):

    def apply(self, query, value):
        return query.where(self.column == value)

    def operation(self):
        return 'equals'


class ApiRuleAdmin(AdminPermission, BaseView):
    column_list = ('rule_type', 'rule_info', 'deleted')
    column_searchable_list = ('rule_info',)
    can_export = False
    can_delete = True
    column_default_sort = ('created_at', True)
    # 额外过滤条件
    # Extra filtering conditions
    column_extra_filters = [
        # 类型过滤下拉框
        # Type filter drop-down box
        CustomFilter(
            column=ApiRule.rule_type,
            name=ApiRule.rule_type.verbose_name,
            options=ApiRule.RULE_TYPE_CHOICES
        )
    ]
    # 列表页 字段显示verbose_name值
    # List page field display verbose_name value
    column_labels = BaseView.get_column_labels(ApiRule)
    # 列表页 字段值显示choices值
    # List page field value display choices value
    column_formatters = {
        'rule_type': lambda v, c, m, p: dict(m.RULE_TYPE_CHOICES).get(m.rule_type)
    }

    # 修改前触发
    # Triggered before modification
    def on_model_change(self, form, model, is_created):
        model.rule_info = model.rule_info.strip()
        if model.rule_info == '':
            raise ValidationError(f'请填写 {ApiRule.rule_info.verbose_name} 字段')
        # 校验规则是否已配置，软删除则不校验
        # Check whether the rule has been configured, soft deletion does not need to be checked
        elif model.deleted is False and ApiRuleService.rule_is_exist(model.id, model.rule_type, model.rule_info):
            raise ValidationError('规则已存在')

        super().on_model_change(form, model, is_created)


ApiRuleAdminView = ApiRuleAdmin(ApiRule, endpoint='_api_rule', name='api规则')
