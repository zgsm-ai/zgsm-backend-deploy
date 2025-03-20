#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/9/26 17:11
"""
import logging

from bot.bot_util import compute_tokens
from common.constant import GPTConstant
from common.exception.exceptions import PromptTokensError

logger = logging.getLogger(__name__)

class GenerateCodeBase:
    """For code generation scenarios"""

    @staticmethod
    def check_prompt(prompt):
        """By character length"""
        tokens_num = compute_tokens(prompt)
        if tokens_num > GPTConstant.CODE_GENERATE_MAX_PROMPT_TOKENS:
            logger.info(f'prompt tokens exceeded limit: {tokens_num} > {GPTConstant.CODE_GENERATE_MAX_PROMPT_TOKENS}')
            raise PromptTokensError()
