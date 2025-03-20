#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Fan Liwei 33139
@Date    ：2023/3/16 14:09
"""

from flask import Blueprint
from controllers.response_helper import Result
from lib.session import SessionService

sessions = Blueprint('sessions', __name__)

@sessions.route('/logout', methods=['GET'])
def logout():
    """
    Logout
    ---
    tags:
      - Session Management
    responses:
      200:
        res: Result
    """
    SessionService.logout()
    return Result.success(message='Logout successful')
