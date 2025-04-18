#!/usr/bin/env python
# -*- coding: utf-8 -*-

from services.action.base_service import ActionStrategy
from common.constant import ActionsConstant


class FindBugsStrategy(ActionStrategy):
    name = ActionsConstant.FIND_BUGS

    def get_prompt(self, data):
        prompt_template = self.get_prompt_template()
        return prompt_template.format(language=data.language,
                                      custom_instructions=data.custom_instructions,
                                      selectedText=data.code)
