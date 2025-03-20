#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Brief introduction

    :Author: Chen Xuan 42766
    :Time: 2023/3/17 15:30
    :Modifier: Chen Xuan 42766
    :UpdateTime: 2023/3/17 15:30
"""

# js to ts question initial template
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
