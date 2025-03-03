#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/16 20:33
    :修改者: 苏德利 16646
    :更新时间: 2023/3/16 20:33
"""

import pytz
from datetime import datetime
from third_platform.es.base_es import BaseESService, calc_rid

class PromptESService(BaseESService):
    """操作记录es"""
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
        插入prompt请求数据，插入异常不影响主流程执行
        :param data: 接口请求参数信息
        :param response_content: 接口请求content返回
        :param usage: 接口消耗的tokens
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
            self.logger.error(f"es插入prompt数据失败，失败日志： {str(err)}")


prompt_es_service = PromptESService()
