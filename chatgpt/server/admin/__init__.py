#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import send_from_directory
from flask_admin import Admin
from flask_admin.base import AdminIndexView

from .auth import AdminIndexView as MainIndexView
from .base import BaseView
from .views import api_rule_admin, configuration_admin, users_admin

runtime_path = os.path.dirname(os.path.realpath(__file__))


def init_admin(app):
    # Initialize admin panel
    admin = Admin(app=app, name="Qianliu Admin", index_view=MainIndexView(), template_mode='bootstrap4')

    # Register system services
    register_view(admin)
    return admin


def register_view(admin: Admin):
    # Register admin views
    admin.add_view(users_admin.UsersAdmin())
    admin.add_view(api_rule_admin.ApiRuleAdmin())
    admin.add_view(configuration_admin.ConfigurationAdmin())

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(runtime_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
