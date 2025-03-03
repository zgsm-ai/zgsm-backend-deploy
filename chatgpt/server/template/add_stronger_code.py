#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 生成健壮代码模板
INITIAL_PROMPT = """
```{language}
{selectedText}
```
Please make the above code more robust, covering more edge cases and handling errors.
Including but not limited to the following points:
1. Function input check supplement: function input check judgment
2. Function/Property call return value check Supplement: Function call or object property return value check
3. Add exception handling logic: Add exception handling logic, such as try cache
4. Do not change the business scenario of the original code

Requirements:
1. Return only one block of code, without any other explanation, using markdown
Output example:
```python
print(123)
```
Output:
"""
