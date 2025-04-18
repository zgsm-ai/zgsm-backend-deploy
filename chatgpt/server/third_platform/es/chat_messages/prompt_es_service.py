#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from third_platform.es.base_es import BaseESService, calc_rid

class PromptESService(BaseESService):
    """Operation record es"""
    def __init__(self):
        super(PromptESService, self).__init__()
        self.index = "prompt"

    @staticmethod
    def _calc_rid(data):
        return calc_rid(data.get("conversation_id", ""),
                        data.get("chat_id", ""),
                        data.get("action", "chat"))

    def insert_prompt(self, data, response_content='', usage=None):
        """
        Insert prompt request data, insert exceptions do not affect the main process execution
        :param data: Interface request parameter information
        :param response_content: Interface request content return
        :param usage: Interface consumption tokens
        """
        try:
            rid = data.get("id")
            if rid is None:
                rid = PromptESService._calc_rid(data)
            if rid and self.es.exists(index=self.index, id=rid):
                self.update_by_id(id=rid, update_data={'is_accept': data.get('isAccept', False),
                                               'accept_num': data.get('acceptNum', 0)})
            else:
                obj_dict = {
                    **data,
                    "id": rid,
                    "usage": usage,
                    "response": response_content
                }
                obj_dict["finish_at"] = datetime.now(pytz.timezone('Asia/Shanghai'))
                self.insert(obj_dict, id=rid)
        except Exception as err:
            self.logger.error(f"es failed to insert prompt data, failure log: {str(err)}")


prompt_es_service = PromptESService()
