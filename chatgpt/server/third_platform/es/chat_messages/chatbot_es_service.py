#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class ChatbotESService(BaseESService):
    """记录与模型对话的关键信息"""
    def __init__(self):
        super(ChatbotESService, self).__init__()
        self.index = "chatbot"

    @staticmethod
    def _calc_rid(data):
        """
        根据用户上报信息中的conversation_id,chat_id,action三个字段计算记录ID
        """
        return calc_rid(data.get("conversation_id", ""), data.get("chat_id", ""), data.get("action", ""))

    def insert_chat_completion(self, data, request_data, response_content=''):
        """
        插入chat.completion调用的记录，这是和对话模型直接通讯的结果记录
        """
        try:
            data["response_content"] = response_content
            self.insert(data, id=self._calc_rid(request_data))
        except Exception as err:
            self.logger.error(f"chatbot.insert_chat_completion插入数据失败，失败日志： {str(err)}")

chatbot_es = ChatbotESService()
