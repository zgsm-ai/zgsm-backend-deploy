#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 14:09
"""

from flask import Blueprint
from controllers.response_helper import Result
from lib.session import SessionService

sessions = Blueprint('sessions', __name__)

@sessions.route('/logout', methods=['GET'])
def logout():
    """
    登出
    ---
    tags:
      - 会话管理
    responses:
      200:
        res: 结果
    """
    SessionService.logout()
    return Result.success(message='登出成功')
