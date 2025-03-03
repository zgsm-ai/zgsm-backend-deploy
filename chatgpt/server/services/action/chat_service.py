#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 陈烜 42766
    :更新时间: 2023/3/24 14:12
"""
from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class ChatStrategy(ActionStrategy):
    name = ActionsConstant.CHAT

    def get_prompt(self, data):
        return data.prompt
