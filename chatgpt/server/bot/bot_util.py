#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tiktoken

from common.constant import GPTModelConstant, GPTConstant

# encoding = tiktoken.get_encoding(TikTokenEncodeType.CL100K_BASE)

def compute_tokens(text: str) -> int:
    """Calculate the number of tokens"""
    # Note that this loading consumes significant memory (1.4GB), load it only when needed, and requires internet access...
    encoding = tiktoken.encoding_for_model(GPTModelConstant.GPT_TURBO)
    tokens_num = len(encoding.encode(text))
    return tokens_num

def get_prompt_max_tokens(model: str) -> int:
    """
    Get the token limit based on the model
    """
    if model in [GPTModelConstant.GPT_4, GPTModelConstant.GPT_4o]:
        return GPTConstant.GPT4_MAX_TOKENS
    return GPTConstant.GPT35_16K_MAX_TOKENS
