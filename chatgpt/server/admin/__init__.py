#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import send_from_directory
from flask_admin import Admin

from .auth import AdminIndexView
from .views import Views

runtime_path = os.path.dirname(os.path.realpath(__file__))


def register_admin(app):
    admin = Admin(app, name='Shenma', template_mode='bootstrap3', index_view=AdminIndexView())
    admin.add_views(*Views)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(runtime_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
