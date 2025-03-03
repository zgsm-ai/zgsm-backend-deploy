#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/20 15:24
"""
import json
import logging

from flask import flash
from flask_admin.actions import action
from wtforms import ValidationError

from admin.auth import AdminPermission
from admin.base import BaseView
from common.constant import ConfigurationConstant
from common.utils.util import re_get_string_in_text
from models.system.configuration import Configuration
from services.system.configuration_service import ConfigurationService


class ConfigurationAdmin(AdminPermission, BaseView):
    column_list = ('belong_type', 'attribute_key', 'attribute_value', 'desc', 'deleted')
    column_searchable_list = ('belong_type', 'attribute_key', 'desc')
    can_export = False
    # 列表页 字段显示verbose_name值
    column_labels = BaseView.get_column_labels(Configuration)

    # 修改前触发
    def on_model_change(self, form, model, is_created):
        if model.belong_type == ConfigurationConstant.PROMPT_TYPE \
                and model.attribute_key == ConfigurationConstant.PROMPT_KEY_FORBID_STRING:
            attribute_value = model.attribute_value
            if attribute_value == '':
                raise ValidationError('属性值不能为空')
            elif len(attribute_value) > ConfigurationConstant.PROMPT_RE_MAX_LENGTH:
                raise ValidationError(f'属性值字符长度限制 {ConfigurationConstant.PROMPT_RE_MAX_LENGTH}')
            try:
                re_get_string_in_text(attribute_value, 'abc')  # 验证正则是否合法，会不会报错
            except Exception as e:
                logging.error(e)
                raise ValidationError('属性值正则不合法')

            ConfigurationService.evict_cache()  # 清除缓存
        elif model.attribute_key == ConfigurationConstant.LANGUAGE_KEY_MAP:
            try:
                json.loads(model.attribute_value)
            except Exception as e:
                logging.error(e)
                raise ValidationError('json格式不正确')

        super().on_model_change(form, model, is_created)

    def after_model_change(self, form, model, is_created=False):
        # 更新后清理广告配置缓存
        if model.attribute_key == ConfigurationConstant.LANGUAGE_KEY_MAP:
            ConfigurationService.evict_language_map_cache()
        else:
            # 通用清理缓存
            ConfigurationService.clear_cache(model.belong_type, model.attribute_key)

    # 清除广告缓存按钮
    @action('clear_ad_cache', '清除用户广告缓存')
    def clear_ad_cache(self, ids):
        ConfigurationService.evict_user_ad_cache()
        flash('广告缓存清除成功')


ConfigurationAdminView = ConfigurationAdmin(Configuration, endpoint='_configuration', name='配置项')
