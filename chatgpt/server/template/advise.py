#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generate next operation suggestions
ADVISE_PROMPT = """
```
{query}
```
Related code:
```{language}
{code}
```

The above information is the operation requested by the user in the previous step. Based on the above information, please generate suggestions for the next operation:
1. These suggestions are closely related to the above information
2. These suggestions are the operations that most users are most likely to perform next

Requirements:
1. Refer to the output example to output the result in JSON format
2. The output format is a JSON array, and the array elements are JSON objects, each object containing the title and prompt fields
3. The output result should not contain any other content except the JSON array, including but not limited to comments, explanations, descriptions, etc.
4. The title field should be concise, preferably within 7 characters, and expressed in Chinese
5. The prompt field needs to contain complete and accurate Chinese prompt information to facilitate the large language model to output higher quality output content
6. The output array should not exceed 7 elements

Output example:

[{{"title": "注释", "prompt": "给以下代码生成注释"}}, {{"title": "检查参数", "prompt": "给以下代码生成检查参数有效性代码"}}]

Output:
"""
