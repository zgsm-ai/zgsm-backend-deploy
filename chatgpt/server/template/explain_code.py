#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/3 17:34
    :修改者: 苏德利 16646
    :更新时间: 2023/3/3 17:34
"""

# 解释代码初始提问模板
INITIAL_PROMPT = """
## Instructions
Summarize the code below (emphasizing its key functionality).
{custom_instructions}.

## Selected Code
```
{selectedText}
```

## Task
Summarize the code at a high level (including goal and purpose) with an emphasis on its key functionality.
Must reply with Chinese.

## Response
"""

# 解释代码连续提问模板
RESPONSE_PROMPT = """
## Instructions
Continue the conversation below.
Pay special attention to the current developer request.

## Current Request
Developer: {{lastMessage}}

{{#if selectedText}}
## Selected Code
```
{{selectedText}}
```
{{/if}}

## Code Summary
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
