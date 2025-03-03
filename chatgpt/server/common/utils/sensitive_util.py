#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 敏感词处理工具
@Author  : 黄伟伦w82676
@Date    : 2024/5/31 15:45
"""
import re

from common.constant import PromptConstant


def sensitization_process(text):
    """
    敏化处理
    text: 需要敏化的文本
    """

    for target_word, replace_word in PromptConstant.SENSITIVE_WORD_MAP.items():
        if target_word in text:
            text = re.sub(target_word, replace_word, text)
    return text


def desensitization_process(text):
    """
    脱敏处理
    text: 需要脱敏的文本
    """
    for target_word, replace_word in PromptConstant.TARGET_WORD_MAP.items():
        if target_word in text:
            text = re.sub(target_word, replace_word, text)
    return text
