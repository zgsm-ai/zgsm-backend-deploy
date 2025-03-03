#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 11:26
"""

from dao.base_dao import BaseDao
from models.system.prompt_square import PromptSquare


class PromptSquareDao(BaseDao):
    model = PromptSquare
