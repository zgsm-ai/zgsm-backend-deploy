#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .api_rule_admin import ApiRuleAdmin
from .configuration_admin import ConfigurationAdmin
from .users_admin import UsersAdmin

Views = [
    UsersAdmin,
    ConfigurationAdmin,
    ApiRuleAdmin,
]
