#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 10:55
"""
import logging
import os
import re
from datetime import datetime

from common.exception.exceptions import FieldValidateError
from common.helpers.application_context import ApplicationContext
from dao.system.prompt_square_dao import PromptSquareDao
from services.base_service import BaseService

PATTERN_USERNAME = re.compile(r'\d{5}|admin')


class PromptSquareService(BaseService):
    dao = PromptSquareDao
    logger = logging.getLogger(__name__)

    @classmethod
    def list(cls, *args, **kwargs):
        # search参数 模糊匹配title，不区分大小写
        search = kwargs.get("search")
        if search:
            conditions = (cls.dao.model.title ** f'{cls.dao.model.like(search)}',)
            kwargs['conditions'] = conditions
        return super().list(*args, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        title = kwargs.get('title')
        _, total = PromptSquareService.dao.list(title=title)
        if total > 0:
            raise FieldValidateError('已存在相同标题，请修改后重试。')
        # 换行符拼接多问题prompt
        kwargs['prompt'] = os.linesep.join([item.get('prompt') for item in kwargs.get('prompt_completion')])
        user = ApplicationContext.get_current()
        kwargs['creator'] = user.display_name
        res = super().get_or_create(**kwargs)
        return res

    @classmethod
    def update(cls, mid, **kwargs):
        if 'title' in kwargs:
            _, total = cls.dao.list(title=kwargs.get('title'))
            if total > 0:
                raise FieldValidateError('已存在相同标题，请修改后重试。')

        kwargs['update_at'] = datetime.now()
        result = PromptSquareService.update_by_id(mid, **kwargs)
        if isinstance(result, dict) or not result:
            return result
        return result.dict()

    @classmethod
    def validate_fields(cls, fields):
        """校验创建数据参数"""
        rules = [
            {'label': 'title', 'type': str, 'name': '标题'},
            {'label': 'prompt_completion', 'type': list, 'name': '问答'}
        ]
        return cls._validate(fields, rules)

    @classmethod
    def validate_update_fields(cls, mid, fields):
        """校验更新时的参数"""
        rules = [
            {"label": "title", "type": str, 'name': '标题'},
        ]
        return cls._validate(fields, rules)


class PromptSquareHotService(BaseService):
    dao = PromptSquareDao
    logger = logging.getLogger(__name__)

    @classmethod
    def update(cls, mid, **kwargs):
        # 更新热度
        if 'use' in kwargs:
            kwargs.pop('use')
            kwargs['hot'] = cls.dao.model.hot + 1

        result = PromptSquareService.update_by_id(mid, **kwargs)
        if isinstance(result, dict) or not result:
            return result
        return result.dict()

    @classmethod
    def validate_update_fields(cls, mid, fields):
        """校验更新时的参数"""
        rules = [
            {"label": "use", "type": bool, 'name': '热度'},
        ]
        return cls._validate(fields, rules)


prompt_square_service = PromptSquareService()
prompt_square_hot_service = PromptSquareHotService()
