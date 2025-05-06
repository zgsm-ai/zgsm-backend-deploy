#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Initial template for identifying potential issues in code
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
Must reply with English.

## Analysis
"""

# Continuous query template for identifying potential issues in code
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
Must reply with English.

## Response
Bot:
"""
