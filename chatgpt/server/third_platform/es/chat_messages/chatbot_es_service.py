#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class ChatbotESService(BaseESService):
    """Record key information of conversation with the model"""
    def __init__(self):
        super(ChatbotESService, self).__init__()
        self.index = "chatbot"

    @staticmethod
    def _calc_rid(data):
        """
        Calculate record ID based on conversation_id, chat_id, and action fields from user reported information
        """
        return calc_rid(data.get("conversation_id", ""), data.get("chat_id", ""), data.get("action", ""))

    def insert_chat_completion(self, data, request_data, response_content=''):
        """
        Insert records of chat.completion calls, which are the result records of direct communication with the dialog model
        """
        try:
            data["response_content"] = response_content
            self.insert(data, id=self._calc_rid(request_data))
        except Exception as err:
            self.logger.error(f"chatbot.insert_chat_completion data insertion failed, error log: {str(err)}")

chatbot_es = ChatbotESService()
