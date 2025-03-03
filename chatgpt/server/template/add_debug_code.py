#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成调试代码模板
INITIAL_PROMPT = """
```{language}
{selectedText}
```
Please make the above code easier to debug:
1. Add some log statements

Requirements:
1. Do not change the original code logic
2. Return only one block of code, using markdown
Output example:
```python
print(123)
```
Output:
"""
