#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.constant import ActionsConstant, ConfigurationConstant
from services.action.base_service import ActionStrategy


class ReviewStrategy(ActionStrategy):
    name = ActionsConstant.REVIEW

    def get_prompt(self, data):
        # 这里使用主动review模板
        prompt_template = self.get_prompt_template(attribute_key=ConfigurationConstant.MANUAL_REVIEW_PROMPT)
        # 组合prompt
        language = data.language
        code = data.code
        return prompt_template.format(language=language,
                                      custom_instructions=data.custom_instructions,
                                      selectedText=code)
