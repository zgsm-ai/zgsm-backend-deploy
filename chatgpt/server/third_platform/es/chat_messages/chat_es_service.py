#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService
from datetime import datetime
import pytz

class ChatESService(BaseESService):
    """Record key information of websocket communication"""
    def __init__(self):
        super(ChatESService, self).__init__()
        self.index = "chat"

    def insert_connect(self, sid, user):
        """
        Record websocket connection information
        """
        try:
            data = {
                "username": user.username,
                "display_name": user.display_name,
                "host_ip": getattr(user, "host_ip", ""),
                "connect_time": datetime.now(pytz.timezone('Asia/Shanghai'))
            }
            self.insert(data, id=sid)
        except Exception as e:
            self.logger.error(f'ES operation chat.connect data failed, error log: {str(e)}')

    def insert_chat(self, sid, data: dict):
        """
        Record request conversation information sent by the client through websocket
        """
        try:
            exist = self.es.exists(index=self.index, id=sid)
            if not exist:
                self.insert(data, id=sid)
            else:
                self.update_by_id(id=sid, update_data=data)
        except Exception as e:
            self.logger.error(f'ES operation chat data failed, error log: {str(e)}')

chat_es = ChatESService()
