#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/17 15:30
    :修改者: 陈烜 42766
    :更新时间: 2023/3/17 15:30
"""

# js转ts提问初始模板
INITIAL_PROMPT = """
I will give you the code written in {language}, and you should optimize and translate them into TypeScript.
Consider overall readability and idiomatic constructs, and optimize the code where possible.
Only provide an optimized version of the code.
{custom_instructions}
Your responses should only contain the code, and should not include any additional explanations or instructions.
```
{selectedText}
```
"""

RESPONSE_PROMPT = ""
