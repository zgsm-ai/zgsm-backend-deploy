#!/usr/bin/env python
# -*- coding: utf-8 -*-

from services.action.base_service import ActionStrategy, process_retract
from services.action.generate_code_base_service import GenerateCodeBase
from common.constant import ActionsConstant


class SimplifyCodeStrategy(GenerateCodeBase, ActionStrategy):
    name = ActionsConstant.SIMPLIFY_CODE

    def get_prompt(self, data):
        prompt_template = self.get_prompt_template()
        return prompt_template.format(language=data.language,
                                      selectedText=data.code)

    @process_retract
    def make_result(self, *args, **kwargs):
        return super().make_result(*args, **kwargs)
