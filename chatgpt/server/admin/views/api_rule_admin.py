#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    # Additional filter conditions
    column_extra_filters = [
        # Type filter dropdown
        CustomFilter(
            column=ApiRule.rule_type,
            name=ApiRule.rule_type.verbose_name,
            options=ApiRule.RULE_TYPE_CHOICES
        )
    ]
    # List page field display verbose_name value
    column_labels = BaseView.get_column_labels(ApiRule)
    # List page field value display choices value
    column_formatters = {
        'rule_type': lambda v, c, m, p: dict(m.RULE_TYPE_CHOICES).get(m.rule_type)
    }

    # Triggered before modification
    def on_model_change(self, form, model, is_created):
        model.rule_info = model.rule_info.strip()
        if model.rule_info == '':
            raise ValidationError(f'Please fill in the {ApiRule.rule_info.verbose_name} field')
        # Check if the rule is already configured, no check for soft delete
        elif model.deleted is False and ApiRuleService.rule_is_exist(model.id, model.rule_type, model.rule_info):
            raise ValidationError('Rule already exists')

        super().on_model_change(form, model, is_created)


ApiRuleAdminView = ApiRuleAdmin(ApiRule, endpoint='_api_rule', name='API Rules')
