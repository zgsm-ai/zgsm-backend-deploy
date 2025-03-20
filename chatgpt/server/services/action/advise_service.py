#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : zbc
@Date    : 2024/11/20 08:53
"""
from services.action.base_service import ActionStrategy, ChatbotOptions
from services.agents.agent_data_classes import ChatRequestData

class AdviseStrategy(ActionStrategy):
    """
    LLM gives the most likely next step recommendation
    """
    name = 'advise'

    def get_model(self, options: ChatbotOptions = None):
        return 'deepseek-chat'

    def get_prompt(self, data: ChatRequestData):
        prompt_template = self.get_prompt_template()
        return prompt_template.format(
            language=data.language,
            query=data.query,
            code=data.code,
            selectedText=data.code,
            commentLanguage=data.comment_language,
        )

    def make_result(self, data: ChatRequestData, options: ChatbotOptions = None):
        if not options:
            options = ChatbotOptions()
        full_data = ""
        res = self.ask(data, options=options)
        for chunk_data in res:
            if not chunk_data:
                continue
            full_data += chunk_data
        return full_data
