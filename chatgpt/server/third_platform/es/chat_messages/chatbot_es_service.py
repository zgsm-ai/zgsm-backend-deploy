#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class ChatbotESService(BaseESService):
    """Record key information about conversations with the model"""
    def __init__(self):
        super(ChatbotESService, self).__init__()
        self.index = "chatbot"

    @staticmethod
    def _calc_rid(data):
        """
        Calculate the record ID based on the conversation_id, chat_id, and action fields in the user-reported information
        """
        return calc_rid(data.get("conversation_id", ""), data.get("chat_id", ""), data.get("action", ""))

    def insert_chat_completion(self, data, request_data, response_content=''):
        """
        Insert the record of chat.completion calls, which is the result record of direct communication with the dialogue model
        """
        try:
            data["response_content"] = response_content
            self.insert(data, id=self._calc_rid(request_data))
        except Exception as err:
            self.logger.error(f"chatbot.insert_chat_completion failed to insert data, error log: {str(err)}")

chatbot_es = ChatbotESService()
