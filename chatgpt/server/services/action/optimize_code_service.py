#!/usr/bin/env python
# -*- coding: utf-8 -*-

from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class OptimizeCodeStrategy(ActionStrategy):
    name = ActionsConstant.OPTIMIZE

    def get_prompt(self, data):
        prompt_template = self.get_prompt_template()
        return prompt_template.format(language=data.language,
                                      custom_instructions=data.custom_instructions,
                                      selectedText=data.code)
