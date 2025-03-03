#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 划词对话合并代码提问模板
"""
现在有两份代码，一份是原本的代码；一份是增加需求后有一些改动的代码，
但是这份代码中部分在原本代码中出现过的被省略掉了，请将第二份代码对照第一份代码修复合并为一份最终可用的代码
Now there are two copies of the code, one is the original code;
One is the code with some changes after the increase of requirements,
but some of the code that appears in the original code has been omitted,
please repair the second code and merge the first code into a final usable code
"""
MERGE_CODE_PROMPT = """## Instructions
You are now a senior front-end engineer.
The output consists of three parts: the requirements, the original code, and the developed code.
Background: The developed code is based on the original code and develops the content mentioned in the requirements
Your task can be summarized as follows:
1.Compare the original code and the developed code, and record the differences.
2.Identify the omission markers in the developed code.
3.Based on the omission markers, find the corresponding omitted code in the original code.
4.Copy the omitted code into the developed code.
5.Verify if the newly added code can produce the correct results.
6.Finally, complete the developed code is used as the output.
Let's think step by step about the solution.
The programming language is {language}.
The output should be concise, professional, and in Markdown code block format (see output sample format).

## input
### requirements
{requirements}

### original code
{original_code}

### developed code
{developed_code}

## output sample format
```vue
code
```

## output"""
