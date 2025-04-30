#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from json import JSONDecodeError

from common.constant import ConfigurationConstant, PromptConstant, ADConstant
from dao.system.configuration_dao import ConfigurationDao
from lib.cache.cache_anno import cache_able, cache_evict, cache_all_evict
from services.base_service import BaseService
from template import DEFAULT_TEMPLATE_MAP
from config import conf

logger = logging.getLogger(__name__)


class ConfigurationService(BaseService):
    dao = ConfigurationDao
    CACHE_KEY_PREFIX = ConfigurationConstant.CACHE_KEY_PREFIX
    CACHE_KEY_FORBID_WORD = PromptConstant.CACHE_KEY_FORBID_WORD
    CACHE_KEY_LANGUAGE_MAP = ConfigurationConstant.CACHE_KEY_LANGUAGE_MAP

    @classmethod
    def get_list(cls, **kwargs):
        attribute_key = kwargs.get('attribute_key')
        total = 1
        if attribute_key == ConfigurationConstant.LANGUAGE_KEY_MAP:
            data_list = cls.get_language_map(kwargs)
        else:
            query, total = cls.dao.list(**kwargs)
            data_list = [data.dict() for data in query]

            for item in data_list:
                try:
                    # 若是json字符串，则进行反序列化
                    item['attribute_value'] = json.loads(item['attribute_value'])
                except JSONDecodeError:
                    pass

        return data_list, total

    @classmethod
    def get_configuration(cls, belong_type, attribute_key, default=None):
        """通用查询"""
        kwargs = {
            'belong_type': belong_type,
            'attribute_key': attribute_key,
            'is_need_total': False,  # 节省一次统计查询
        }
        query, _ = cls.dao.list(**kwargs)
        return query[0].attribute_value if query and len(query) > 0 else default

    @classmethod
    @cache_able(CACHE_KEY_PREFIX, index=[1, 2])
    def get_configuration_with_cache(cls, belong_type, attribute_key, default=None):
        """通用查询缓存"""
        res = cls.get_configuration(belong_type, attribute_key, default)
        return res

    @classmethod
    @cache_evict(CACHE_KEY_PREFIX, index=[1, 2])
    def clear_cache(cls, belong_type, attribute_key):
        """通用清理缓存"""
        logging.info(f"clear_cache {cls.CACHE_KEY_PREFIX}:{belong_type}:{attribute_key}")

    @classmethod
    def get_prompt_template(cls, attribute_key):
        """查询prompt模板，有缓存"""
        default = DEFAULT_TEMPLATE_MAP.get(attribute_key, '')
        prompt = cls.get_configuration_with_cache(ConfigurationConstant.PROMPT_TEMPLATE, attribute_key, default)
        return prompt

    @classmethod
    def get_prompt_forbidden_word(cls):
        return cls.get_configuration_with_cache(ConfigurationConstant.PROMPT_TYPE,
                                                ConfigurationConstant.PROMPT_KEY_FORBID_STRING,
                                                None)

    @classmethod
    @cache_evict(CACHE_KEY_FORBID_WORD)
    def evict_cache(cls):
        logger.info('清理禁用敏感词缓存')
        return

    @classmethod
    @cache_all_evict(ADConstant.CACHE_PREFIX_KEY)
    def evict_user_ad_cache(cls):
        logger.info('清理用户广告记录缓存')
        return

    @classmethod
    @cache_able(CACHE_KEY_LANGUAGE_MAP)
    def get_language_map(cls, kwargs):
        data = cls.dao.get_or_none(**kwargs)
        if data:
            return json.loads(data.attribute_value)
        else:
            return []

    @classmethod
    @cache_all_evict(CACHE_KEY_LANGUAGE_MAP)
    def evict_language_map_cache(cls):
        logger.info('清理语言映射缓存')
        return

    @classmethod
    def get_system_config(cls):
        try:
            data = json.loads(cls.get_configuration_with_cache(ConfigurationConstant.SYSTEM_TYPE,
                                                               ConfigurationConstant.SYSTEM_KEY,
                                                               '{}'))
        except JSONDecodeError:
            data = {'error': 'json error'}
        return data

    @classmethod
    def get_model_ide_normal(cls, attribute_key):
        """根据action端的配置获取model"""
        data = cls.dao.get_or_none(belong_type=attribute_key, attribute_key=attribute_key)
        if data:
            return data.attribute_value
        else:
            return conf.get('default_model_name', 'deepseek-chat')

