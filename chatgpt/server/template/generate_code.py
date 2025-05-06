#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Initial template for code generation query
INITIAL_PROMPT = """
## Instructions
Generate code for the following specification.
{custom_instructions}.

## Specification
{content}

## Instructions
Generate code for the specification.
Must reply with English.

## Code
"""


# Template for form code generation
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

# Template for Q&A code generation
ASK_PROMPT = """
## Instructions
Now you are a senior development engineer .
Generate code for the following Code .
{custom_instructions}
Must reply with English and show me the code in your answer .

## Code
```
{code}
```
"""
