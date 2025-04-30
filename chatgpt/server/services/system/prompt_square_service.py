#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        # search parameter for fuzzy matching title, case insensitive
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
            raise FieldValidateError('Title already exists, please modify and try again.')
        # Join multiple question prompts with newline characters
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
                raise FieldValidateError('Title already exists, please modify and try again.')

        kwargs['update_at'] = datetime.now()
        result = PromptSquareService.update_by_id(mid, **kwargs)
        if isinstance(result, dict) or not result:
            return result
        return result.dict()

    @classmethod
    def validate_fields(cls, fields):
        """Validate create data parameters"""
        rules = [
            {'label': 'title', 'type': str, 'name': 'Title'},
            {'label': 'prompt_completion', 'type': list, 'name': 'Q&A'}
        ]
        return cls._validate(fields, rules)

    @classmethod
    def validate_update_fields(cls, mid, fields):
        """Validate update parameters"""
        rules = [
            {"label": "title", "type": str, 'name': 'Title'},
        ]
        return cls._validate(fields, rules)


class PromptSquareHotService(BaseService):
    dao = PromptSquareDao
    logger = logging.getLogger(__name__)

    @classmethod
    def update(cls, mid, **kwargs):
        # Update hotness
        if 'use' in kwargs:
            kwargs.pop('use')
            kwargs['hot'] = cls.dao.model.hot + 1

        result = PromptSquareService.update_by_id(mid, **kwargs)
        if isinstance(result, dict) or not result:
            return result
        return result.dict()

    @classmethod
    def validate_update_fields(cls, mid, fields):
        """Validate update parameters"""
        rules = [
            {"label": "use", "type": bool, 'name': 'Hotness'},
        ]
        return cls._validate(fields, rules)


prompt_square_service = PromptSquareService()
prompt_square_hot_service = PromptSquareHotService()
