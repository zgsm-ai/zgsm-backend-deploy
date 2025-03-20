#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Chen Xuan 42766
    :Time: 2023/3/24 14:12
    :Modifier: Chen Xuan 42766
    :UpdateTime: 2023/3/24 14:12
"""
from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class FindBugsStrategy(ActionStrategy):
    name = ActionsConstant.FIND_BUGS

    def get_prompt(self, data):
        prompt_template = self.get_prompt_template()
        return prompt_template.format(language=data.language,
                                      custom_instructions=data.custom_instructions,
                                      selectedText=data.code)
