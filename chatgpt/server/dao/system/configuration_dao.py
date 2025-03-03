#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/4/20 10:56
"""
from dao.base_dao import BaseDao
from models.system.configuration import Configuration


class ConfigurationDao(BaseDao):
    model = Configuration
