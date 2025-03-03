#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService

class UseCodeESService(BaseESService):
    """记录用户反馈的使用LLM所生成代码的行为"""
    def __init__(self):
        super(UseCodeESService, self).__init__()
        self.index = "use_code"

use_code_es = UseCodeESService()
