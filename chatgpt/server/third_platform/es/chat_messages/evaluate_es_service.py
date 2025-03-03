#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService

class EvaluateESService(BaseESService):
    """记录用户反馈的对话评价"""
    def __init__(self):
        super(EvaluateESService, self).__init__()
        self.index = "evaluate"

evaluate_es = EvaluateESService()
