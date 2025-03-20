#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Sudeli 16646
    :Time: 2023/3/3 17:34
    :Modifier: Sudeli 16646
    :UpdateTime: 2023/3/3 17:34
"""

# Initial template for asking questions to find potential problems in the code
INITIAL_PROMPT = """
## Instructions
What could be wrong with the code below?
Only consider defects that would lead to incorrect behavior.
The programming language is {language}.
{custom_instructions}

## Selected Code
```
{selectedText}
```

## Task
Describe what could be wrong with the code?
Only consider defects that would lead to incorrect behavior.
Provide potential fix suggestions where possible.
Consider that there might not be any problems with the code."
Include code snippets (using Markdown) and examples where appropriate.
Must reply with Chinese.

## Analysis
"""

# Continuous question template for finding potential problems in the code
RESPONSE_PROMPT = """
## Instructions
Continue the conversation below.
Pay special attention to the current developer request.
The programming language is {language}.
{custom_instructions}.

## Current Request
Developer: {lastMessage}

{{#if selectedText}}
## Selected Code
```
{{selectedText}}
```
{{/if}}

## Potential Bugs
{{firstMessage}}

## Conversation
{{#each messages}}
{{#if (neq @index 0)}}
{{#if (eq author "bot")}}
Bot: {{content}}
{{else}}
Developer: {{content}}
{{/if}}
{{/if}}
{{/each}}

## Task
Write a response that continues the conversation.
Stay focused on current developer request.
Consider the possibility that there might not be a solution.
Ask for clarification if the message does not make sense or more input is needed.
Use the style of a documentation article.
Omit any links.
Include code snippets (using Markdown) and examples where appropriate.
Must reply with Chinese.

## Response
Bot:
"""
