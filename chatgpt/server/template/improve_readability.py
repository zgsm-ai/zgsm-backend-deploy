#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/3 17:35
    :修改者: 苏德利 16646
    :更新时间: 2023/3/3 17:35
"""

# 优化代码初始提问模板
INITIAL_PROMPT = """
## Instructions
How could the readability of the code below be improved?
The programming language is {language}.
Consider overall readability and idiomatic constructs.
{custom_instructions}.

## Selected Code
```
{selectedText}
```

## Task
How could the readability of the code be improved?
The programming language is {language}.
Consider overall readability and idiomatic constructs.
Provide potential improvements suggestions where possible.
Consider that the code might be perfect and no improvements are possible.
Include code snippets (using Markdown) and examples where appropriate.
The code snippets must contain valid {language} code.
Must reply with Chinese.

## Readability Improvements
"""

# 优化代码连续提问模板
RESPONSE_PROMPT = """
## Instructions
Continue the conversation below.
Pay special attention to the current developer request.
The programming language is {{language}}.

## Current Request
Developer: {{lastMessage}}

{{#if selectedText}}
## Selected Code
```
{{selectedText}}
```
{{/if}}

## Conversation
{{#each messages}}
{{#if (eq author "bot")}}
Bot: {{content}}
{{else}}
Developer: {{content}}
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
The code snippets must contain valid {{language}} code.
Must reply with Chinese.

## Response
Bot:
"""
