#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 9:38
"""

import logging
import jwt

from flask import request
from lib.jwt_session.session import session

logger = logging.getLogger(__name__)

def get_username_by_token(token: str): 
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded.get("preferred_username")

class ApplicationContext:
    """
    上下文,用在RESTAPI中,用于管理与服务交互的用户信息
    """
    @classmethod
    def get_session(cls):
        return session

    @classmethod
    def get_current(cls, raise_not_found_exception=True, auth=None):
        api_key = cls._get_api_key()
        if api_key:
            user = cls._get_user_by_api_key(api_key)
            if user:
                return user
        from services.system.users_service import UsersService
        # 尝试通过三种手段获取username：会话缓存，api_key，authorization
        username = cls.get_current_username()
        if not username and api_key:
            #  已经通过用户系统的认证，获得了token
            username = get_username_by_token(api_key)
        if not username:
            #  没token，也没username，创建一个test用户顶着用，当是匿名登录
            user = UsersService.create_test_user()
            ApplicationContext.update_session_user(user)
            return user
        user = UsersService().get_by_username(username)
        if user:
            return user
        user = UsersService.create_zgsm_user(username, "", "", api_key)
        if user:
            ApplicationContext.update_session_user(user)
            return user
        if raise_not_found_exception:
            # 放头部会出现循环导入 导致异常
            from common.exception.exceptions import NoLoginError
            raise NoLoginError()
        return user

    @classmethod
    def _get_api_key(cls):
        """
        从请求中获取api_key
        """
        api_key = request.args.get("api-key") if not request.headers.get(
            "api-key") else request.headers.get("api-key")
        if not api_key:
            # for socket
            if hasattr(request, "event"):
                auth = request.event.get("args", [{}])[-1]
                api_key = auth.get("api-key")
        return api_key

    @classmethod
    def _get_user_by_api_key(cls, api_key):
        from services.system.users_service import UsersService
        try:
            user = UsersService.get_user_by_api_key(api_key)
            return user
        except Exception as err:
            logger.error(f"解析api_key：{api_key}出现异常:{str(err)}")
        return None

    @classmethod
    def get_cookie(cls):
        return request.headers.get("cookie")

    @classmethod
    def get_access_ip(cls):
        if request.headers.get('X-Forwarded-For') is not None:
            ips = str(request.headers.get('X-Forwarded-For'))
            _ip = ips.split(",")[0]
        elif request.headers.get('X-Real-IP') is not None:
            _ip = str(request.headers.get('X-Real-IP'))
        else:
            _ip = str(request.remote_addr)
        return _ip

    @classmethod
    def get_current_username(cls):
        username = session.get("username")
        if username:
            return username
        return None

    @classmethod
    def get_current_app_id(cls):
        return request.headers.get('app-id')

    @classmethod
    def clear_session(cls):
        session.clear()

    @classmethod
    def update_session_attr(cls, maps):
        if maps:
            for key in maps.keys():
                session[key] = maps[key]

    @classmethod
    def reset_session(cls, data):
        cls.clear_session()
        cls.update_session_attr(data)

    @classmethod
    def update_session_user(cls, user):
        session['username'] = user.username

    @classmethod
    def update_username(cls, username):
        session['username'] = username
