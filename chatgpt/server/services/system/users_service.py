#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    users对应的service业务逻辑层

    :作者: 苏德利 16646
    :时间: 2023/3/14 16:01
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 16:01
"""
import logging
import re

from flask import g

from common.constant import UserConstant, AnalysisConstant
from common.utils.util import generate_random_avatar_color
from dao.system.users_dao import UsersDao
from services.base_service import BaseService
from lib.cache.cache_anno import cache_able, cache_evict, cache_all_evict
from common.utils.encrypt import encode_by_base64
from lib.lock import lock_check, RedisLock

PATTERN_USERNAME = re.compile(r'\d{5}|admin')


class UsersService(BaseService):
    dao = UsersDao
    logger = logging.getLogger(__name__)
    CACHE_KEY_API_KEY = UserConstant.CACHE_KEY_API_KEY
    CACHE_KEY_ID = UserConstant.CACHE_KEY_ID
    CACHE_KEY_USERNAME = UserConstant.CACHE_KEY_USERNAME
    CACHE_KEY_WORK_ID = AnalysisConstant.CACHE_KEY_WORK_ID

    @classmethod
    def create_test_user(cls):
        """
        创建测试用户，测试和开发环境使用
        """
        avatar_color = generate_random_avatar_color()
        search_kw = {
            'username': 'test',
            'display_name': 'test'
        }
        defaults = {
            **search_kw,
            'avatar_color': avatar_color
        }
        return cls.get_or_create_v2(**search_kw, defaults=defaults)
    
    @classmethod
    def create_zgsm_user(cls, username, display_name, host_ip, token):
        """
        创建诸葛神码的用户
        """
        avatar_color = generate_random_avatar_color()
        search_kw = {
            'username': username
        }
        defaults = {
            **search_kw,
            'avatar_color': avatar_color,
            'display_name': display_name,
            "description": host_ip,
            'api_key': token
        }
        return cls.get_or_create_v2(**search_kw, defaults=defaults)

    @classmethod
    def update_api_key(cls, user):
        cls.evict_user_cache(user.id, user.username, user.api_key)
        new_api_key = encode_by_base64(f"{user.display_name}")
        cls.dao.update_by_id(user.id, api_key=new_api_key)
        result = cls.dao.get_by_id(user.id)
        return result

    @classmethod
    @cache_evict(CACHE_KEY_ID, index=[1])
    @cache_evict(CACHE_KEY_USERNAME, index=[2])
    @cache_evict(CACHE_KEY_API_KEY, index=[3])
    @cache_evict(CACHE_KEY_WORK_ID, index=[2])
    def evict_user_cache(cls, user_id, username, api_key):
        cls.logger.info(f'清理用户缓存:{username}')
        return user_id, username, api_key

    @classmethod
    @cache_all_evict(CACHE_KEY_ID)
    @cache_all_evict(CACHE_KEY_USERNAME)
    @cache_all_evict(CACHE_KEY_API_KEY)
    @cache_all_evict(CACHE_KEY_WORK_ID)
    def clear_all_user_cache(cls):
        """清除所有用户相关数据"""
        cls.logger.info('清理所有用户缓存')
        return

    @classmethod
    def get_or_create_by_username_and_display_name(cls, username, display_name, email=None):
        """慎用,并发操作时调用，防止创建多个用户"""
        username = str(username)
        if len(username) not in [5, 6]:
            cls.logger.info(f'用户名不合法: {username}')
            return None
        match = PATTERN_USERNAME.findall(username)
        if match:
            if email is None:
                email = f'{match[0]}@sangfor.com'
            user = cls.get_by_username(username)
            if not user:
                user = cls.__lock_get_or_create(username, display_name, email)
            return user
        cls.logger.info(f'用户名不合法: {username}')
        return None

    @classmethod
    @lock_check(RedisLock(5), prefix='lock_user', index=[1])
    def __lock_get_or_create(cls, username, display_name, email, is_admin=False):
        """慎用,并发操作时调用，防止创建多个用户"""
        api_key = encode_by_base64(f"{display_name}")
        avatar_color = generate_random_avatar_color()
        search_kw = {
            'username': username,
            'display_name': display_name
        }
        defaults = {
            **search_kw,
            'email': email,
            'is_admin': is_admin,
            'avatar_color': avatar_color,
            'api_key': api_key
        }
        user = cls.get_or_create_v2(**search_kw, defaults=defaults)
        return user

    @classmethod
    @cache_able(CACHE_KEY_API_KEY, index=[1])
    def get_user_by_api_key(cls, api_key):
        """
        :param username: 用于cache缓存key
        :param api_key: 解析用的
        :return:
        """
        user_obj = cls.dao.get_or_none(api_key=api_key)
        return user_obj

    @classmethod
    @cache_able(CACHE_KEY_USERNAME, index=[1])
    def get_by_username(cls, username):
        return cls.dao.get_or_none(username=username)

    @classmethod
    def get_by_email(cls, email):
        return cls.dao.get_or_none(email=email)

    @classmethod
    def get_by_display_name(cls, display_name):
        return cls.dao.get_or_none(display_name=display_name)

users_service = UsersService()
