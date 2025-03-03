#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/7 16:35
    :修改者: 苏德利 16646
    :更新时间: 2023/3/7 16:35
"""

# 生成代码的提问初始模板
INITIAL_PROMPT = """
## Instructions
Generate code for the following specification.
{custom_instructions}.

## Specification
{content}

## Instructions
Generate code for the specification.
Must reply with Chinese.

## Code
"""


# 表单生成代码的模板
FORM_PROMPT = """
## Instructions
Now you are a Senior Programmer.
Generate results based on the following requirements.
The results must use {program_stack}.
The results content type : {generation_type}.
using Markdown format, and identify its coding language to specify

## Requirement
{custom_instructions}
{input_instructions}
{output_instructions}
## results
"""

# 问答生成代码的模板
ASK_PROMPT = """
## Instructions
Now you are a senior development engineer .
Generate code for the following Code .
{custom_instructions}
Must reply with Chinese and show me the code in your answer .

## Code
```
{code}
```
"""
