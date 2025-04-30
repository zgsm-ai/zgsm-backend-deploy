#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import peewee
from flask_admin.model.form import InlineFormAdmin
from wtforms.validators import DataRequired

from common.exception.error_code import ERROR_CODE
from models.api_rule import APIRule, ApiRuleDimension, ApiRuleDimensionRel
from models.configuration import Configuration
from ..base import BaseView
from datetime import datetime

logger = logging.getLogger(__name__)

class CustomFilter(BasePeeweeFilter):

    def apply(self, query, value):
        return query.where(self.column == value)

    def operation(self):
        return 'equals'


class ApiRuleDimensionInline(InlineFormAdmin):
    form_args = dict(
        dimension=dict(validators=[DataRequired()]),
        dimension_value=dict(validators=[DataRequired()])
    )
    form_choices = {
        'dimension': [
            ('ip', 'IP'),
            ('user_id', 'User ID'),
            ('domain', 'Domain'),
            ('host', 'Host'),
            ('query_content', 'Query Content'),
        ]
    }


class ApiRuleAdmin(BaseView):
    column_labels = dict(
        id='ID',
        title='Title',
        model='Model',
        status='Status',
        date_created='Created At',
        date_updated='Updated At',
        description='Description',
        api_rule_dimensions='Control Dimensions',
        is_white='Is Whitelist',
        expire_date='Expiration Date',
        rule_type='Rule Type',
    )
    column_list = ('id', 'title', 'model', 'status', 'date_created', 'date_updated', 'expire_date')
    column_filters = ('id', 'title', 'model', 'status', 'date_created', 'date_updated', 'expire_date')
    column_searchable_list = ('title', 'model', 'description')
    column_formatters = {}
    column_sortable_list = ('id', 'date_created', 'date_updated')
    form_excluded_columns = ('date_created', 'date_updated')
    inline_models = (ApiRuleDimensionInline(ApiRuleDimensionRel),)
    form_choices = {
        'status': [
            ('0', 'Disabled'),
            ('1', 'Enabled'),
        ],
        'model': [
            ('*', 'All Models'),
            ('gpt-3.5-turbo', 'GPT-3.5'),
            ('gpt-4', 'GPT-4'),
        ],
        'rule_type': [
            ('0', 'Content Control'),
            ('1', 'Request Control'),
        ],
        'is_white': [
            ('0', 'Blacklist'),
            ('1', 'Whitelist'),
        ],
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.date_created = datetime.now()
        model.date_updated = datetime.now()


ApiRuleAdminView = ApiRuleAdmin(ApiRule, endpoint='_api_rule', name='api规则')
