#!/usr/bin/env python
# -*- coding: utf-8 -*-
from third_platform.es.base_es import BaseESService

class EvaluateESService(BaseESService):
    """Record user feedback conversation evaluations"""
    def __init__(self):
        super(EvaluateESService, self).__init__()
        self.index = "evaluate"

evaluate_es = EvaluateESService()
