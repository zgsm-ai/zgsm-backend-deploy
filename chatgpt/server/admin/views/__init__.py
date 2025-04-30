#!/usr/bin/env python
# -*- coding: utf-8 -*-

from admin.views.api_rule_admin import ApiRuleAdminView
from admin.views.configuration_admin import ConfigurationAdminView
from admin.views.users_admin import UsersView

Views = [
    UsersView,
    ConfigurationAdminView,
    ApiRuleAdminView,
]
