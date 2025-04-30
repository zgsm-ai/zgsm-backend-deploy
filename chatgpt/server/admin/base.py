# -*- coding: utf-8 -*-

from flask import redirect, request, url_for
from flask_admin import BaseView as OriginBaseView
from flask_admin.contrib.peewee import ModelView, filters
from flask_admin.model import filters as modelFilters
from peewee import CharField, ForeignKeyField
from wtforms import StringField
from wtforms.widgets import TextArea


class CustomFilterConverter(filters.FilterConverter):
    # Support additional number fields
    @modelFilters.convert('ForeignKeyField', 'AutoField', 'SmallIntegerField')
    def conv_extra_num(self, column, name):
        return [f(column, name) for f in self.int_filters]

    # Support additional JSON fields
    @modelFilters.convert('JSONField')
    def conv_json(self, column, name):
        return [f(column, name) for f in self.strings]


class AdminView:
    def is_accessible(self):
        # return can_login()
        # FIXME temporarily open
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index', next=request.url))


class ActionView(AdminView, OriginBaseView):
    SUCCESS_PAGE = 'admin/success.html'


class BaseView(AdminView, ModelView):
    can_export = True
    can_delete = False
    can_view_details = True
    filter_converter = CustomFilterConverter()
    column_extra_filters = []
    column_extra_searchable_list = []

    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.init_column_filters()
        self.init_column_searches()
        super(BaseView, self).__init__(model, *args, **kwargs)

    def init_column_filters(self):
        if self.column_filters:
            return
        column_extra_filters_fields = [field.column.name for field in self.column_extra_filters]
        filters = list()
        for field in self.model._meta.sorted_fields:
            field_name = f'{field.name}_id' if isinstance(field, ForeignKeyField) else field.name
            # If the extra filter rewrites this field, do not use the default filtering rule for this field
            if field_name not in column_extra_filters_fields:
                filters.append(field_name)
        self.column_filters = filters + self.column_extra_filters

    def init_column_searches(self):
        if self.column_searchable_list:
            return
        searches = list()
        for field in self.model._meta.sorted_fields:
            if isinstance(field, CharField):
                searches.append(field.name)
        self.column_searchable_list = searches + self.column_extra_searchable_list

    def get_all_data(self):
        # Get filter conditions
        view_args = self._get_list_extra_args()
        # Sort
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]
        # Get data and total (specify 0 for no pagination)
        return self.get_list(0, sort_column, view_args.sort_desc,
                             view_args.search, view_args.filters, page_size=0)

    @staticmethod
    def get_column_labels(model_):
        """
        Field:verbose_name display mapping
        return: e.g., {'username': 'User Account'}
        """
        attrs = model_._meta.fields
        column_labels = {}
        for column in attrs:
            # If there is no verbose_name, use the current field name
            verbose_name = attrs.get(column).verbose_name if attrs.get(column).verbose_name else column
            column_labels[column] = verbose_name
        return column_labels


class CustomTextAreaField(StringField):
    """Text type edit box"""
    widget = TextArea()
