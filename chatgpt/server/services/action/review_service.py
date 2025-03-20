#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    simple introduction

    :Author: Chen Xuan 42766
    :Time: 2023/3/24 14:12
    :Modifier: Chen Xuan 42766
    :UpdateTime: 2023/3/24 14:12
"""
from common.constant import ActionsConstant, ConfigurationConstant
from services.action.base_service import ActionStrategy


class ReviewStrategy(ActionStrategy):
    name = ActionsConstant.REVIEW

    def get_prompt(self, data):
        # Here use active review template
        prompt_template = self.get_prompt_template(attribute_key=ConfigurationConstant.MANUAL_REVIEW_PROMPT)
        # Combination prompt
        language = data.language
        code = data.code
        return prompt_template.format(language=language,
                                      custom_instructions=data.custom_instructions,
                                      selectedText=code)
