#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 公共函数抽取模板
INITIAL_PROMPT = """
```{language}
{selectedText}
```
This code could be chunked into smaller functions and extracts the common function, which would look like:
"""
