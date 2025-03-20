#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Fan Liwei 33139
@Date    ：2023/3/16 9:37
"""

import logging
import secrets

from common.helpers.application_context import ApplicationContext

class SessionService:
    logger = logging.getLogger(__name__)
    # pylint: disable=no-member
    config = {}

    @classmethod
    def gen_state(cls, length=32):
        """
        Generate a random state to prevent CSRF
        """
        return secrets.token_urlsafe(nbytes=length)[0:length]

    @classmethod
    def logout(cls):
        user = ApplicationContext.get_current()
        if user:
            ApplicationContext.clear_session()
