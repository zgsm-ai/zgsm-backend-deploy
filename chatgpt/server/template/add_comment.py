#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成注释模板
INITIAL_PROMPT = """
```{language}
{selectedText}
```
Please add {commentLanguage} comments to the above code:
1. The comments of the function describe its function, parameters, return values, and examples
2. Include sensible comments at key points

Requirements:
1. Comments should follow the comment format of the language standard document
2. Return only one block of code, using markdown
3. If there are spaces or tabs before the given code,
 the generated code should retain those spaces or tabs at the beginning of each line.

Output example:
```python
print(123)
```
Output:
"""
