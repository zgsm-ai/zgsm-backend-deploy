#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 10:58
"""
import logging
from functools import wraps


from common.exception.exceptions import AuthFailError
from common.helpers.application_context import ApplicationContext

logger = logging.getLogger(__name__)


class PermissionChecker:
    """
    Permission check
    """

    def __init__(self):
        pass

    @staticmethod
    def check_is_admin_or_creator(service):
        """Check if it is a super administrator or creator"""

        def outer(func):
            @wraps(func)
            def has_permission(*args, **kwargs):
                user = ApplicationContext.get_current()
                creator = service.get_by_id(kwargs.get('mid'))
                if not user or not creator:
                    raise AuthFailError(msg="You do not have permission to perform this operation.")
                elif not user.is_admin and user.display_name != creator.creator:
                    raise AuthFailError(msg="You do not have permission to perform this operation.")
                return func(*args, **kwargs)

            return has_permission

        return outer
