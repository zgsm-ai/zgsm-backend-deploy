#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/30 14:22
"""
from admin.views.api_rule_admin import ApiRuleAdminView
from admin.views.configuration_admin import ConfigurationAdminView
from admin.views.users_admin import UsersView

Views = [
    UsersView,
    ConfigurationAdminView,
    ApiRuleAdminView,
]
