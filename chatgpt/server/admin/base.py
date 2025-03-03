# -*- coding: utf-8 -*-
'''
@Author: 刘铭哲w10458
@Date: 2020-12-15 10:40:20
'''

from flask import redirect, request, url_for
from flask_admin import BaseView as OriginBaseView
from flask_admin.contrib.peewee import ModelView, filters
from flask_admin.model import filters as modelFilters
from peewee import CharField, ForeignKeyField
from wtforms import StringField
from wtforms.widgets import TextArea


class CustomFilterConverter(filters.FilterConverter):
    # 支持额外的数字字段
    @modelFilters.convert('ForeignKeyField', 'AutoField', 'SmallIntegerField')
    def conv_extra_num(self, column, name):
        return [f(column, name) for f in self.int_filters]

    # 支持额外的JSON字段
    @modelFilters.convert('JSONField')
    def conv_json(self, column, name):
        return [f(column, name) for f in self.strings]


class AdminView:
    def is_accessible(self):
        # return can_login()
        # FIXME 暂时放开
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
            # 如果额外过滤器重写该字段，则不使用该字段默认过滤规则
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
        # 获取过滤条件
        view_args = self._get_list_extra_args()
        # 排序
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]
        # 获取数据与总数(指定0不分页)
        return self.get_list(0, sort_column, view_args.sort_desc,
                             view_args.search, view_args.filters, page_size=0)

    @staticmethod
    def get_column_labels(model_):
        """
        字段:verbose_name 显示映射
        return：例：{'username': '用户帐号'}
        """
        attrs = model_._meta.fields
        column_labels = {}
        for column in attrs:
            # 如果没有verbose_name，则使用当前字段名
            verbose_name = attrs.get(column).verbose_name if attrs.get(column).verbose_name else column
            column_labels[column] = verbose_name
        return column_labels


class CustomTextAreaField(StringField):
    """编辑框text类型"""
    widget = TextArea()
