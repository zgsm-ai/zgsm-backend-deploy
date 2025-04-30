#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.utils.util import is_valid_regex
from dao.base_dao import BaseDao
from common.exception.exceptions import ModelException
from common.utils.pxfilter import XssHtml
import logging

XSS_FILTER = XssHtml()


class BaseService:
    dao = BaseDao

    def __init__(self):
        self.model_name = self.dao.model.__name__

    @classmethod
    def get_or_create(cls, **kwargs):
        logging.info(f"get_or_create {cls.dao.model.__name__},kwargs:{kwargs}")
        return cls.dao.get_or_create(**kwargs)

    @classmethod
    def get_or_create_v2(cls, **kwargs):
        logging.info(f"get_or_create_v2 {cls.dao.model.__name__},kwargs:{kwargs}")
        return cls.dao.get_or_create_v2(**kwargs)

    @classmethod
    def create_or_update(cls, **kwargs):
        return cls.dao.create_or_update(**kwargs)

    @classmethod
    def validate_fields(cls, fields):
        return True, fields

    @classmethod
    def validate_update_fields(cls, mid, fields):
        return cls.validate_fields(fields)

    @staticmethod
    def _validate(fields, rules):
        """
        rules: {
            label: string,
            optional: boolean,
            type: type,
            allow_false: boolean  # Determine if the field value converted to bool is false
        }[]
        """
        result = dict()

        if not fields:
            fields = dict()

        for r in rules:
            field_key = r['label']
            field_type = r['type']
            field_name = r['name'] if r.__contains__('name') else field_key
            allow_empty = r['allow_empty']if r.__contains__('allow_empty') else False
            optional = r.__contains__('optional') and r['optional']
            # Specified as rich text field, need to do xss filtering
            is_rich = r.__contains__('is_rich') and r['is_rich']
            # Validate length
            length = r['length'] if r.__contains__('length') else None
            contain = fields.__contains__(field_key)
            is_empty = not contain or fields.get(field_key) in [None, '']
            allow = r['allow_false'] if r.__contains__('allow_false') else True
            field_is_exist = field_key in fields

            if not optional and not field_is_exist:
                return False, f'[{field_name}] : This field cannot be empty'
            elif not optional and is_empty and not allow_empty:
                return False, f'[{field_name}] : This input item cannot be empty'
            if not allow and contain and not bool(fields.get(field_key)):
                # If the field is included, and the conversion to bool is False, not_false is set to True
                return False, f'[{field_name}] : This input item cannot be empty'
            if contain and fields[field_key] and field_type == 're_str' and fields[field_key]:
                if not is_valid_regex(fields[field_key]):
                    return False, f'[{field_name}] field value is not a valid regex'
            elif contain and fields[field_key] and not isinstance(fields[field_key], field_type):
                if field_type is bool and fields[field_key].lower() in ['true', 'false']:
                    result[field_key] = True if fields[field_key].lower() == 'true' else False
                return False, f'[{field_name}] field type should be {field_type.__name__}'
            if contain and isinstance(fields[field_key], str) and isinstance(length, int):
                # Validate length
                if len(fields[field_key]) > length:
                    return False, f'[{field_name}] : This input item length cannot exceed {length}'
            if not contain:
                continue
            result[field_key] = fields[field_key]
            if is_rich and (field_type is str or isinstance(result[field_key], str)):
                result[field_key] = XSS_FILTER.filter(result[field_key])
            # xxx_id fields, if falsy, force set to None
            if field_type is int and field_key[-3:] == '_id' and not fields[field_key]:
                result[field_key] = None
        return True, result

    @classmethod
    def create(cls, **kwargs):
        logging.info(f"Creating {cls.dao.model.__name__},kwargs:{kwargs}")
        return cls.dao.create(**kwargs)

    @classmethod
    def delete_by_id(cls, mid):
        logging.info(f"Deleting {cls.dao.model.__name__},id:{mid}")
        return cls.dao.delete_by_id(mid)

    @classmethod
    def recover_by_id(cls, mid):
        logging.info(f"Recovering {cls.dao.model.__name__},id:{mid}")
        return cls.dao.recover_by_id(mid)

    @classmethod
    def update_by_id(cls, mid, **kwargs):
        logging.info(f"Updating {cls.dao.model.__name__},id:{mid},kwargs:{kwargs}")
        # Before updating, check if the resource exists
        cls.get_by_id(mid)
        cls.dao.update_by_id(mid, **kwargs)
        result = cls.get_by_id(mid)
        return result

    @classmethod
    def get_by_id(cls, mid):
        return cls.dao.get_by_id(mid)

    @classmethod
    def list(cls, *args, **kwargs):
        """
        By default, get entries with deleted field set to False
        If deleted=None is passed, get all entries
        """
        return cls.dao.list(*args, **kwargs)

    @classmethod
    def gen_info(cls, obj, *args, **kwargs):
        """
        Customize the information to be displayed
        """
        return obj.dict(*args, **kwargs)

    @classmethod
    def valid_unique(cls, like=False, **kwargs):
        """
        Validate uniqueness
        """
        msg = kwargs.pop('msg', None)
        query, total = cls.list(like=like, **kwargs)
        if total > 1:
            raise ModelException(msg if msg else "Operation failed")

    @classmethod
    def set_create_username(cls, kwargs):
        pass

    @classmethod
    def bulk_create(cls, dicts, batch_size=10):
        cls.dao.bulk_create(dicts, batch_size=batch_size)

    @classmethod
    def bulk_delete(cls, conditions=(), **check_fields):
        return cls.dao.bulk_update(check_fields, update_fields=dict(deleted=True), conditions=conditions)

    @classmethod
    def count(cls, conditions=(), **kwargs):
        return cls.dao.get_nums(conditions=conditions, **kwargs)

    @classmethod
    def process_time_range_query(cls, field_name: str, start_time: str = '', end_time: str = '') -> tuple:
        """Process time range query expressions"""
        conditions = ()
        if start_time:
            conditions += (getattr(cls.dao.model, field_name) >= start_time,)
        if end_time:
            conditions += (getattr(cls.dao.model, field_name) < end_time,)
        return conditions
