#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import DoesNotExist, Model, fn

from common.constant import NullValueSort, AppConstant
from common.exception.exceptions import ModelException, NoResourceError


class NotImplementsModel(Exception):
    pass


class BaseDao:
    model = Model

    # pylint: disable=no-member

    @classmethod
    def get_or_create(cls, **kwargs):
        query, total = cls.list(**kwargs)
        kwargs.pop('include_fields', None)
        if total == 0:
            return cls.model.create(**kwargs)
        return query.get()

    @classmethod
    def get_or_create_v2(cls, **kwargs):
        """
        Separate query conditions and insert data
        kwargs['defaults']: insert data
        other parameters: query conditions
        """
        defaults = kwargs.pop('defaults', {})
        query, total = cls.list(**kwargs)
        kwargs.pop('include_fields', None)
        if total == 0:
            return cls.model.create(**defaults)
        return query.get()

    @classmethod
    def create(cls, **kwargs):
        obj = cls.model.create(**kwargs)
        return obj

    @classmethod
    def delete_by_id(cls, mid):
        return cls.update_by_id(mid, deleted=True)

    @classmethod
    def recover_by_id(cls, mid):
        return cls.update_by_id(mid, deleted=False)

    @classmethod
    def update_by_id(cls, mid, **kwargs):
        """
        Can retrieve object even after soft deletion
        """
        cls.model.update(**kwargs).where(cls.model.id == mid).execute()

    @classmethod
    def create_or_update(cls, **kwargs):
        """
        Separate query conditions and insert/update data
        kwargs['defaults']: insert/update data
        other parameters: query conditions
        """
        defaults = kwargs.pop('defaults', {})
        query = cls.get_or_none(**kwargs)
        if not query:
            return cls.model.create(**defaults)
        cls.update_by_id(mid=query.id, **defaults)
        return cls.get_or_none(**kwargs)

    @classmethod
    def get_by_id(cls, mid):
        try:
            return cls.get(id=mid)
        except DoesNotExist:
            raise NoResourceError()

    @classmethod
    def get(cls, deleted=False, **kwargs):
        try:
            if deleted is None:
                return cls.model.get(**kwargs)
            return cls.model.get(deleted=deleted, **kwargs)
        except DoesNotExist:
            raise NoResourceError()

    @classmethod
    def get_or_none(cls, deleted=False, **kwargs):
        try:
            if deleted is None:
                return cls.model.get(**kwargs)
            return cls.model.get(deleted=deleted, **kwargs)
        except DoesNotExist:
            return None

    @classmethod
    def count_sort(cls, column, conditions=(True,), process_query=None, limit=5, min_count=1, order='desc', **kwargs):
        column_field = getattr(cls.model, column, None)
        if not column_field:
            raise ModelException(f'The specified field {column} does not exist in {cls.model}')
        count_field = 'c_count'

        count_column = fn.COUNT(column_field).alias(count_field)
        order_column = count_column
        if order == 'desc':
            order_column = count_column.desc()
        query = cls.model.select(column_field, count_column)
        if process_query and callable(process_query):
            query = process_query(query)
        query = (query
                 .where(*conditions, *cls._parse_kw_to_conditions(kwargs))
                 .group_by(column_field)
                 .order_by(order_column)
                 .having(fn.COUNT(column_field) >= min_count)
                 .limit(limit))
        return [{
            'field': getattr(q, column),
            'count': getattr(q, count_field)
        } for q in query if getattr(q, column, None)]

    @classmethod
    def _parse_kw_to_conditions(cls, kw, like=True):
        # Implement parsing of kw to conditions tuple
        conditions = list()
        if like:
            name = kw.pop('name', None)
            if name:
                conditions.append((fn.LOWER(cls.model.name) % f'{cls.model.like(name.lower())}'))
        ids = kw.pop('ids', None)
        if ids and isinstance(ids, str):
            ids = list(map(int, ids.split(',')))
            conditions.append((cls.model.id << ids))
        elif isinstance(ids, list):
            conditions.append((cls.model.id << ids))
        if kw.__contains__('deleted'):
            if kw['deleted'] is None:
                kw.pop('deleted')
        else:
            kw['deleted'] = False
        for k in kw.keys():
            if getattr(cls.model, k, None):
                kw[k] = cls.boolean_transfrom(getattr(cls.model, k, None), kw[k])
                if isinstance(kw[k], list):
                    conditions.append((getattr(cls.model, k) << kw[k]))
                else:
                    conditions.append((getattr(cls.model, k) == kw[k]))
        return tuple(conditions)

    @classmethod
    def bulk_update(cls, check_fields, update_fields, conditions=(True,)):
        """
        This method is for batch operations, may not be suitable for some scenarios (no operation logs, skipping update_by_id may cause issues in certain scenarios),
        so it is not called in base service, and should be called individually in the corresponding service layer when needed
        """
        conditions = (*conditions, *cls._parse_kw_to_conditions(check_fields))
        for k in update_fields.keys():
            if not getattr(cls.model, k, None):
                update_fields.pop(k)
        cls.model.update(update_fields).where(*conditions).execute()

    @classmethod
    def boolean_transfrom(cls, field, field_value):
        from peewee import BooleanField
        if type(field) is BooleanField:
            if field_value == 'false':
                return False
            if field_value == 'true':
                return True
        return field_value

    @classmethod
    def list(cls, page=None, per=None, conditions=(True,),
             process_query=None, like=True, include_fields=None, **kwargs):
        query = cls.model.select()
        if process_query and callable(process_query):
            query = process_query(query)
        # Extra keyword arguments will be passed to _parse_kw_to_conditions for parsing
        query = query.where(*conditions, *cls._parse_kw_to_conditions(kwargs, like=like))
        # _parse_kw_to_order_by parses sorting parameters
        query = cls._parse_kw_to_order_by(query, kwargs)
        # Whether total is needed, returns 0 if not needed, default is needed
        is_need_total = kwargs.get('is_need_total', True)
        total = 0
        if is_need_total:
            # total returns the total count rather than single page count, calculating total for large data volumes has significant impact on the database
            total = query.count(database=cls.model._meta.database)
        if page and per:
            query = query.paginate(int(page), int(per))
        query = cls.select_model_fields(query, include_fields)
        return query, total

    @classmethod
    def select_model_fields(cls, query, include_fields):
        if include_fields:
            select_fields = []
            for field in include_fields:
                if hasattr(cls.model, field):
                    select_fields.append(eval(f'cls.model.{field}'))
            query = query.select(*select_fields)
        return query

    def delete_by_instance(self, _instance):
        # _instance.delete_instance()
        _instance.deleted = AppConstant.DELETED
        _instance.save()

    @classmethod
    def remove_invalid_fields(cls, fields):
        """
        Remove invalid fields, e.g., '' empty string, '-' illegal character
        """
        # valid_fields = [item[0] for item in self.get_valid_fields(queryset, view, {'request': request})]
        def term_valid(term):
            if term.startswith("-"):
                term = term[1:]
            return term

        return [term for term in fields if term_valid(term)]

    @classmethod
    def get_ordering_value(cls, param, null_param):
        descending = param.startswith('-')
        if descending:
            return getattr(cls.model, param[1:]).desc(**null_param)
        if null_param:
            return getattr(cls.model, param).asc(**null_param)
        return getattr(cls.model, param).asc()

    @classmethod
    def order_by_filter(cls, query, kw):
        params = kw.pop('ordering', None)
        if params:
            sort_null = kw.pop('sort_null', None)
            null_param = {}
            # Whether null values come first
            if sort_null:
                null_param['nulls'] = 'LAST'

            fields = [param.strip() for param in params.split(',')]
            ordering = cls.remove_invalid_fields(fields)
            if ordering:
                ordering = [cls.get_ordering_value(param, null_param) for param in ordering]
                return query.order_by(*ordering)

        # No sorting field, or all sorting fields are invalid
        return query

    @classmethod
    def _parse_kw_to_order_by(cls, query, kw):
        # Multiple field sorting
        if kw.get('ordering'):
            return cls.order_by_filter(query, kw)

        sort_by = kw.pop('sort_by', None)
        sort_to = kw.pop('sort_to', 'asc')
        sort_null = kw.pop('sort_null', None)
        if sort_by and sort_to and getattr(cls.model, sort_by, None):
            if sort_to.lower() == 'desc':
                if sort_null == NullValueSort.NULL_LAST:
                    return query.order_by(getattr(cls.model, sort_by).desc(nulls='LAST'))
                query = query.order_by(getattr(cls.model, sort_by).desc())
            else:
                if sort_null == NullValueSort.NULL_FIRST:
                    return query.order_by(getattr(cls.model, sort_by).asc(nulls='FIRST'))
                query = query.order_by(getattr(cls.model, sort_by))

        return query

    @classmethod
    def bulk_create(cls, dicts, batch_size=10):
        if not dicts:
            return
        objs = []
        for item in dicts:
            objs.append(cls.model(**item))
        cls.model.bulk_create(objs, batch_size=batch_size)

    @classmethod
    def get_nums(cls, conditions=(True,), process_query=None, like=True, **kwargs, ):
        query = cls.model.select(fn.COUNT(1))
        if process_query and callable(process_query):
            query = process_query(query)
        # Extra keyword arguments will be passed to _parse_kw_to_conditions for parsing
        query = query.where(*conditions, *cls._parse_kw_to_conditions(kwargs, like=like))
        return query.count()
