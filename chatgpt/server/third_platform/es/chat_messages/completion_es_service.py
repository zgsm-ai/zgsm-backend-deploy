#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class CompletionESService(BaseESService):
    """Records key information for code completion services"""
    def __init__(self):
        super(CompletionESService, self).__init__()
        self.index = "completion"

    @staticmethod
    def _calc_rid(data):
        """
        Calculate the record ID, key information includes: completion_id, fpath, line, column, line_prefix
        """
        return calc_rid(data.get("completion_id", ""), 
                        data.get("fpath", ""), 
                        f"{data.get('line')}:{data.get('column')}", 
                        data.get("line_prefix", ""))

    def insert_completion(self, data):
        """
        Insert code completion record
        """
        try:
            self.insert(data, id=self._calc_rid(data))
        except Exception as err:
            self.logger.error(f"completion.insert_completion failed to insert data, failure log: {str(err)}")

    def update_completion(self, data):
        pass

completion_es = CompletionESService()
