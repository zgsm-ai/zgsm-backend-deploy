#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from common.constant import ActionsConstant
from services.action.base_service import ActionStrategy, ChatbotOptions
from services.system.configuration_service import ConfigurationService
from services.agents.agent_data_classes import ChatRequestData

# Zhuge normal chat
class NormalChatStrategy(ActionStrategy):
    name = ActionsConstant.ZHUGE_NORMALCHAT

    def get_model(self, options: ChatbotOptions = None):
        if options.model:
            return options.model
        return ConfigurationService.get_model_ide_normal(self.name)

    def get_prompt(self, data: ChatRequestData):
        return data.prompt

    def make_result(self, data: ChatRequestData, options: ChatbotOptions = None):
        if not options:
            options = ChatbotOptions()
        full_data = ""
        res = self.ask(data, options=options)
        for chunk_data in res:
            if chunk_data:
                full_data += chunk_data
                yield {"event": "message", "answer": chunk_data}
        yield {"event": "sf_tokens", "total_answer": full_data}
