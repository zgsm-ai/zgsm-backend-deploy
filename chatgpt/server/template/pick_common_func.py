#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Common function extraction template
INITIAL_PROMPT = """
```{language}
{selectedText}
```
This code could be chunked into smaller functions and extracts the common function, which would look like:
"""
