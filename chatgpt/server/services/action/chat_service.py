#!/usr/bin/env python
# -*- coding: utf-8 -*-

from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class ChatStrategy(ActionStrategy):
    name = ActionsConstant.CHAT

    def get_prompt(self, data):
        return data.prompt
