#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/3 17:34
    :修改者: 苏德利 16646
    :更新时间: 2023/3/3 17:34
"""

# 查找代码可能存在问题的提问初始模板
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

# 查找代码可能存在问题的连续提问模板
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
