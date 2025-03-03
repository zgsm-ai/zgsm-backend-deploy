#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService
from datetime import datetime
import pytz

class ChatESService(BaseESService):
    """记录websocket通讯的关键信息"""
    def __init__(self):
        super(ChatESService, self).__init__()
        self.index = "chat"

    def insert_connect(self, sid, user):
        """
        记录websocket连接信息
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
            self.logger.error(f'es 操作 chat.connect 数据失败，失败日志： {str(e)}')

    def insert_chat(self, sid, data: dict):
        """
        记录客户端通过websocket发送的请求对话的信息
        """
        try:
            exist = self.es.exists(index=self.index, id=sid)
            if not exist:
                self.insert(data, id=sid)
            else:
                self.update_by_id(id=sid, update_data=data)
        except Exception as e:
            self.logger.error(f'es 操作 chat 数据失败，失败日志： {str(e)}')

chat_es = ChatESService()
