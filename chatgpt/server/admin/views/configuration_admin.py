#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    # List page field display verbose_name value
    column_labels = BaseView.get_column_labels(Configuration)

    # Triggered before modification
    def on_model_change(self, form, model, is_created):
        if model.belong_type == ConfigurationConstant.PROMPT_TYPE \
                and model.attribute_key == ConfigurationConstant.PROMPT_KEY_FORBID_STRING:
            attribute_value = model.attribute_value
            if attribute_value == '':
                raise ValidationError('Attribute value cannot be empty')
            elif len(attribute_value) > ConfigurationConstant.PROMPT_RE_MAX_LENGTH:
                raise ValidationError(f'Attribute value character length limit {ConfigurationConstant.PROMPT_RE_MAX_LENGTH}')
            try:
                # Verify whether the regular expression is legal and whether an error will be reported
                re_get_string_in_text(attribute_value, 'abc')
            except Exception as e:
                logging.error(e)
                raise ValidationError('Invalid regular expression for attribute value')

            ConfigurationService.evict_cache()  # Clear cache
        elif model.attribute_key == ConfigurationConstant.LANGUAGE_KEY_MAP:
            try:
                json.loads(model.attribute_value)
            except Exception as e:
                logging.error(e)
                raise ValidationError('Invalid JSON format')

        super().on_model_change(form, model, is_created)

    def after_model_change(self, form, model, is_created=False):
        # Clear the advertising configuration cache after update
        if model.attribute_key == ConfigurationConstant.LANGUAGE_KEY_MAP:
            ConfigurationService.evict_language_map_cache()
        else:
            # General clear cache
            ConfigurationService.clear_cache(model.belong_type, model.attribute_key)

    # Clear advertisement cache button
    @action('clear_ad_cache', 'Clear User Ad Cache')
    def clear_ad_cache(self, ids):
        ConfigurationService.evict_user_ad_cache()
        flash('Ad cache cleared successfully')


ConfigurationAdminView = ConfigurationAdmin(Configuration, endpoint='_configuration', name='Configuration Items')