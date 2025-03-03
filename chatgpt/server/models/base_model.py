#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 14:16
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 14:16
"""

from playhouse.shortcuts import _clone_set, Field, Alias
from peewee import Model, ForeignKeyField, callable_, SqliteDatabase, BooleanField, DateTimeField
from db import db
from datetime import datetime


class BaseModel(Model):
    dict_exclude = []

    class Meta:
        database = db

    deleted = BooleanField(default=False, verbose_name='软删除')
    created_at = DateTimeField(default=datetime.now, null=True, verbose_name='创建时间')
    update_at = DateTimeField(default=datetime.now, null=True, verbose_name='更新时间')

    def set_key(self):
        if hasattr(self, "key"):
            self.key = f"{self._meta.table_name.replace('tb_', '')}_%0.5d" % self.id
            self.save()
        else:
            raise AttributeError()

    def gen_field_name(self, field_key):
        if field_key == "description":
            return "描述"
        elif field_key == "key":
            return "key"
        elif field_key == "name":
            return "名称"
        elif field_key == "updated_at":
            return "更新时间"
        elif field_key == "updater_username":
            return "更新人"
        elif field_key == "creator_username":
            return "创建人"
        elif field_key == "created_at":
            return "创建时间"
        elif field_key == "status":
            return "状态"
        else:
            return "未知字段"

    @classmethod
    def like(cls, kw):
        if kw:
            kw = kw.replace('%', '\%')  # noqa: W605
            kw = kw.replace('_', '\_')  # noqa: W605
        wildcard = '*' if issubclass(db.obj.__class__, SqliteDatabase) else '%'
        return f'{wildcard}{kw}{wildcard}'

    def dict(self, recurse=True, backrefs=False, only=None,
             exclude=None, seen=None, extra_attrs=None,
             fields_from_query=None, max_depth=None, manytomany=False):
        """
        改写自playhouse.shortcuts.model_to_dict方法
        将其改写成实例方法，并替换掉自身函数调用
        Convert a model instance (and any related objects) to a dictionary.

        :param bool recurse: Whether foreign-keys should be recursed.
        :param bool backrefs: Whether lists of related objects should be recursed.
        :param only: A list (or set) of field instances indicating which fields
            should be included.
        :param exclude: A list (or set) of field instances that should be
            excluded from the dictionary.
        :param list extra_attrs: Names of model instance attributes or methods
            that should be included.
        :param SelectQuery fields_from_query: Query that was source of model. Take
            fields explicitly selected by the query and serialize them.
        :param int max_depth: Maximum depth to recurse, value <= 0 means no max.
        :param bool manytomany: Process many-to-many fields.
        """
        model = self
        max_depth = -1 if max_depth is None else max_depth
        if max_depth == 0:
            recurse = False

        only = _clone_set(only)
        extra_attrs = _clone_set(extra_attrs)
        should_skip = lambda n: (n in exclude) or (only and (n not in only))  # noqa: E731

        if fields_from_query is not None:
            for item in fields_from_query._returning:
                if isinstance(item, Field):
                    only.add(item)
                elif isinstance(item, Alias):
                    extra_attrs.add(item._alias)

        data = {}
        exclude = _clone_set(exclude)
        seen = _clone_set(seen)
        exclude |= seen
        model_class = type(model)

        if manytomany:
            for name, m2m in model._meta.manytomany.items():
                if should_skip(name):
                    continue

                exclude.update((m2m, m2m.rel_model._meta.manytomany[m2m.backref]))
                for fkf in m2m.through_model._meta.refs:
                    exclude.add(fkf)

                accum = []
                for rel_obj in getattr(model, name):
                    accum.append(rel_obj.dict(
                        recurse=recurse,
                        backrefs=backrefs,
                        only=only,
                        exclude=exclude,
                        max_depth=max_depth - 1
                    ))
                data[name] = accum

        for field in model._meta.sorted_fields:
            if should_skip(field):
                continue

            field_data = model.__data__.get(field.name)
            if isinstance(field, ForeignKeyField) and recurse:
                if field_data is not None:
                    seen.add(field)
                    rel_obj = getattr(model, field.name)
                    field_data = rel_obj.dict(
                        recurse=recurse,
                        backrefs=backrefs,
                        only=only,
                        exclude=exclude,
                        seen=seen,
                        max_depth=max_depth - 1
                    )
                else:
                    field_data = None

            data[field.name] = field_data

        if extra_attrs:
            for attr_name in extra_attrs:
                attr = getattr(model, attr_name)
                if callable_(attr):
                    data[attr_name] = attr()
                else:
                    data[attr_name] = attr

        if backrefs and recurse:
            for foreign_key, rel_model in model._meta.backrefs.items():
                if foreign_key.backref == '+':
                    continue
                descriptor = getattr(model_class, foreign_key.backref)
                if descriptor in exclude or foreign_key in exclude:
                    continue
                if only and (descriptor not in only) and (foreign_key not in only):
                    continue

                accum = []
                exclude.add(foreign_key)
                related_query = getattr(model, foreign_key.backref)

                for rel_obj in related_query:
                    accum.append(rel_obj.dict(
                        recurse=recurse,
                        backrefs=backrefs,
                        only=only,
                        exclude=exclude,
                        max_depth=max_depth - 1))

                data[foreign_key.backref] = accum

        return data

    @classmethod
    def update(cls, *args, **kwargs):
        if hasattr(cls, "update_at"):
            kwargs['update_at'] = datetime.now()
        return super().update(*args, **kwargs)
