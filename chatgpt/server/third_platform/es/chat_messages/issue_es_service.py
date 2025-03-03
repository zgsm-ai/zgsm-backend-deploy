#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService, calc_rid

class IssueESService(BaseESService):
    """记录用户反馈的问题报告"""
    def __init__(self):
        super(IssueESService, self).__init__()
        self.index = "issue"

    @staticmethod
    def _calc_rid(data):
        return calc_rid(data.get("category", ""),
                        data.get("description", ""),
                        data.get("number", ""),
                        data.get("username", ""),
                        data.get("screenshot_name", ""))
    
    def insert_issue(self, data):
        """
        记录用户反馈的问题单
        """
        try:
            if data.get("id") is None:
                data["id"] = self._calc_rid(data)
            self.insert(data, id=data["id"])
        except Exception as err:
            self.logger.error(f"issue.insert_issue插入数据失败，失败日志： {str(err)}")

issue_es = IssueESService()
