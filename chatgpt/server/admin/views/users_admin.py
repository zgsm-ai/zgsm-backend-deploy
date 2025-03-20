#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/30 14:36
"""
from flask import flash
from flask_admin.actions import action

from admin.auth import AdminPermission
from admin.base import BaseView
from models.system.users import Users
from services.system.users_service import UsersService


class UsersAdmin(AdminPermission, BaseView):
    column_list = ('username', 'display_name', 'email', 'is_admin', 'is_plus', 'api_key', 'deleted')
    column_searchable_list = ('display_name',)
    can_create = False
    can_export = False
    # list page field display verbose_name value
    column_labels = BaseView.get_column_labels(Users)
    form_widget_args = {
        'username': {'readonly': True},
        'display_name': {'readonly': True},
        'email': {'readonly': True},
        'created_at': {'readonly': True},
        'update_at': {'readonly': True},
    }

    # Define custom buttons
    @action('clear_all_user_cache', 'Clear all user caches')
    def clear_all_user_cache(self, ids):
        UsersService.clear_all_user_cache()
        flash('User cache cleared successfully')

    def after_model_change(self, form, model, is_created=False):
        # Clear user cache after update
        UsersService.evict_user_cache(model.id, model.username, model.api_key)


UsersView = UsersAdmin(Users, endpoint='_users', name='User')
