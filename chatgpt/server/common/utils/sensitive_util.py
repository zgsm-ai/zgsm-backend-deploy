#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from common.constant import PromptConstant


def sensitization_process(text):
    """
    Sensitization processing
    text: The text that needs to be sensitized
    """

    for target_word, replace_word in PromptConstant.SENSITIVE_WORD_MAP.items():
        if target_word in text:
            text = re.sub(target_word, replace_word, text)
    return text


def desensitization_process(text):
    """
    Desensitization processing
    text: The text that needs to be desensitized
    """
    for target_word, replace_word in PromptConstant.TARGET_WORD_MAP.items():
        if target_word in text:
            text = re.sub(target_word, replace_word, text)
    return text
