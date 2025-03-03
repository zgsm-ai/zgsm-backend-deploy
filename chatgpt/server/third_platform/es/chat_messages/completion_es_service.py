#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class CompletionESService(BaseESService):
    """记录代码补全服务的关键信息"""
    def __init__(self):
        super(CompletionESService, self).__init__()
        self.index = "completion"

    @staticmethod
    def _calc_rid(data):
        """
        计算记录ID，关键信息包括：  completion_id, fpath, line, column, line_prefix
        """
        return calc_rid(data.get("completion_id", ""), 
                        data.get("fpath", ""), 
                        f"{data.get('line')}:{data.get('column')}", 
                        data.get("line_prefix", ""))

    def insert_completion(self, data):
        """
        插入代码补全的记录
        """
        try:
            self.insert(data, id=self._calc_rid(data))
        except Exception as err:
            self.logger.error(f"completion.insert_completion插入数据失败，失败日志： {str(err)}")

    def update_completion(self, data):
        pass

completion_es = CompletionESService()
