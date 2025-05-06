#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Initial template for unit test generation query
INITIAL_PROMPT = """
## Instructions
Write a unit test for the code below.
{custom_instructions}

## Selected Code
```
{selectedText}
```

## Task
Write a unit test that contains test cases for the happy path and for all edge cases.
The programming language is {language}.
Must reply with English.

## Unit Test
"""

# Continuous query template for unit test generation
RESPONSE_PROMPT = """
## Instructions
Rewrite the code below as follows: "{{lastMessage}}"

## Code
```
{{temporaryEditorContent}}
```

## Task
Rewrite the code below as follows: "{{lastMessage}}"
Must reply with English.

## Answer
"""
