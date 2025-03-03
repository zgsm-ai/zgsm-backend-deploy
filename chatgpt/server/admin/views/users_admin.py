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
    # 列表页 字段显示verbose_name值
    column_labels = BaseView.get_column_labels(Users)
    form_widget_args = {
        'username': {'readonly': True},
        'display_name': {'readonly': True},
        'email': {'readonly': True},
        'created_at': {'readonly': True},
        'update_at': {'readonly': True},
    }

    # 定义自定义按钮
    @action('clear_all_user_cache', '清除所有用户缓存')
    def clear_all_user_cache(self, ids):
        UsersService.clear_all_user_cache()
        flash('用户缓存清除成功')

    def after_model_change(self, form, model, is_created=False):
        # 更新后清除用户缓存
        UsersService.evict_user_cache(model.id, model.username, model.api_key)


UsersView = UsersAdmin(Users, endpoint='_users', name='用户')
