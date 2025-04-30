#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from functools import wraps


from common.exception.exceptions import AuthFailError
from common.helpers.application_context import ApplicationContext

logger = logging.getLogger(__name__)


class PermissionChecker:
    """
    权限检查
    """

    def __init__(self):
        pass

    @staticmethod
    def check_is_admin_or_creator(service):
        """校验是否是超管或创建者"""

        def outer(func):
            @wraps(func)
            def has_permission(*args, **kwargs):
                user = ApplicationContext.get_current()
                creator = service.get_by_id(kwargs.get('mid'))
                if not user or not creator:
                    raise AuthFailError(msg="您没有此操作权限。")
                elif not user.is_admin and user.display_name != creator.creator:
                    raise AuthFailError(msg="您没有此操作权限。")
                return func(*args, **kwargs)

            return has_permission

        return outer
