#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.configuration import Configuration


class ConfigurationDao(BaseDao):
    model = Configuration
