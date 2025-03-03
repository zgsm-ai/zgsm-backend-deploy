#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/10/16 11:54
"""

import tiktoken

from common.constant import GPTModelConstant, GPTConstant

# encoding = tiktoken.get_encoding(TikTokenEncodeType.CL100K_BASE)

def compute_tokens(text: str) -> int:
    """计算 token 数"""
    # 注意这个加载需要消耗较大内存（1.4GB），使用的时候再加载，且需要访问外网...
    encoding = tiktoken.encoding_for_model(GPTModelConstant.GPT_TURBO)
    tokens_num = len(encoding.encode(text))
    return tokens_num

def get_prompt_max_tokens(model: str) -> int:
    """
    根据模型获取 限制 token数
    """
    if model in [GPTModelConstant.GPT_4, GPTModelConstant.GPT_4o]:
        return GPTConstant.GPT4_MAX_TOKENS
    return GPTConstant.GPT35_16K_MAX_TOKENS
