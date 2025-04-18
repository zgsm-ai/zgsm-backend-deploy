#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.prompt_square import PromptSquare


class PromptSquareDao(BaseDao):
    model = PromptSquare
