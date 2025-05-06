#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from bot.bot_util import compute_tokens
from common.constant import GPTConstant
from common.exception.exceptions import PromptTokensError

logger = logging.getLogger(__name__)

class GenerateCodeBase:
    """针对代码生成场景"""

    @staticmethod
    def check_prompt(prompt):
        """按字符长度"""
        tokens_num = compute_tokens(prompt)
        if tokens_num > GPTConstant.CODE_GENERATE_MAX_PROMPT_TOKENS:
            logger.info(f'prompt tokens 超限: {tokens_num} > {GPTConstant.CODE_GENERATE_MAX_PROMPT_TOKENS}')
            raise PromptTokensError()
