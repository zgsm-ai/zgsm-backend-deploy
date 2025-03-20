#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 9:42
"""

import logging

from flask import request, make_response

from common.helpers.application_context import ApplicationContext
from config import conf
from lib.jwt_session.session import JwtTokenHandler, JwtSession

logger = logging.getLogger(__name__)


def register_controller(app=None):
    from .system.session_controller import sessions
    from .system.users_controller import users
    from .system.prompt_square_controller import prompt_square
    from controllers.system.configuration_controller import configuration
    from .V4.action_controller import actions_v4
    from controllers.feedback.action_controller import feedbacks

    app.register_blueprint(sessions, url_prefix='/api/sessions')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(prompt_square, url_prefix='/api/prompt_square')
    app.register_blueprint(configuration, url_prefix='/api/configuration')
    app.register_blueprint(actions_v4, url_prefix='/api/v4')
    app.register_blueprint(feedbacks, url_prefix="/api/feedbacks")

    @app.before_request
    def check_request():
        """
        根据规则校验请求是否能够通过, 校验登录
        """
        # Check whether the request can pass according to the rules, check the login status
        pass

    @app.after_request
    def add_header(response):
        return response


NAME = conf.get("jwt", {}).get("NAME")
ALG = conf.get("jwt", {}).get("ALGORITHM")
EXP = conf.get("jwt", {}).get("EXPIRE")
SECRET = conf.get("jwt", {}).get("SECRET")
DOMAIN = conf.get("jwt", {}).get("DOMAIN")


def registry_session(app):
    from services.system.users_service import users_service

    @app.before_request
    def before_request():
        headers = request.headers
        cookies = request.cookies
        app_id = ApplicationContext.get_current_app_id()
        jwt_handler = JwtTokenHandler(
            headers, cookies, NAME, SECRET, EXP, domain=DOMAIN, algorithm=ALG)
        # 解析获得session
        # Parse to get session
        session = jwt_handler.parse()
        if isinstance(session, JwtSession):
            # 查询或者创建用户
            # Query or create user
            username = session.get('username')
            display_name = session.get('display_name')
            user = users_service.get_or_create_by_username_and_display_name(
                username, display_name)
            if not user:
                # 用户非法,清空session
                # User is illegal, clear the session
                ApplicationContext.clear_session()
                return
        ApplicationContext.reset_session(session)

    @app.after_request
    def after_request(response):
        from common.exception.exceptions import NoLoginError
        try:
            try:
                user = ApplicationContext.get_current()
            except NoLoginError:
                user = None
            if user:
                # 用户登录才设置jwt_token
                # Set jwt_token only when the user logs in
                from services.system.jwt_token_service import JwtTokenService
                j_t = JwtTokenService(request)
                jwt_token = j_t.gen_token()
                domain = None if DOMAIN == 'current' else DOMAIN
                data = dict(
                    expires=j_t.get_expire(EXP)
                )
                response.set_cookie(
                    NAME, jwt_token, **data)
                if domain:
                    data.update(domain=domain)

                    response.set_cookie(
                        NAME, jwt_token, **data)
        except Exception as err:
            logger.info(f'生成jwt_token失败：{str(err)}')
            # 该后置请求出现任何异常认为是认证失败, 不做处理，返回原请求
            # Any exception in this post request is considered as authentication failure, no processing is done, and the original request is returned
            pass
        finally:
            return response
