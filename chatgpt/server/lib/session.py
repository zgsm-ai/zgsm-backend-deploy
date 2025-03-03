#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 9:37
"""

import logging
import requests
from urllib import parse
import secrets

from common.helpers.application_context import ApplicationContext
from services.system.users_service import UsersService
from config import conf


class SessionService:
    logger = logging.getLogger(__name__)
    # pylint: disable=no-member
    config = {}

    @classmethod
    def gen_state(cls, length=32):
        """
        生成随机的state，防止csrf
        """
        return secrets.token_urlsafe(nbytes=length)[0:length]

    @classmethod
    def logout(cls):
        user = ApplicationContext.get_current()
        if user:
            ApplicationContext.clear_session()

