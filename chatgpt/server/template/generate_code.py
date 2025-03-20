#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    simple introduction

    :author: Sudeli 16646
    :time: 2023/3/7 16:35
    :modifier: Sudeli 16646
    :update_time: 2023/3/7 16:35
"""

# The initial template for generating code questions
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


# Template for form generation code
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

# Template for question and answer generation code
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
