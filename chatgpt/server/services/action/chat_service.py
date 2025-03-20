#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Chen Xuan 42766
    :Time: 2023/3/24 14:12
    :Modifier: Chen Xuan 42766
    :UpdateTime: 2023/3/24 14:12
"""
from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class ChatStrategy(ActionStrategy):
    name = ActionsConstant.CHAT

    def get_prompt(self, data):
        return data.prompt
