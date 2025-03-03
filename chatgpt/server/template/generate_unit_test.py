#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/3 17:35
    :修改者: 苏德利 16646
    :更新时间: 2023/3/3 17:35
"""

# 生成单元测试初始提问模板
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
Must reply with Chinese.

## Unit Test
"""

# 生成单元测试连续提问模板
RESPONSE_PROMPT = """
## Instructions
Rewrite the code below as follows: "{{lastMessage}}"

## Code
```
{{temporaryEditorContent}}
```

## Task
Rewrite the code below as follows: "{{lastMessage}}"
Must reply with Chinese.

## Answer
"""
