#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Template for extracting common functions
INITIAL_PROMPT = """
```{language}
{selectedText}
```
This code could be chunked into smaller functions and extracts the common function, which would look like:
"""
