#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generate next-step suggestions
ADVISE_PROMPT = """
```
{query}
```
Related code:
```{language}
{code}
```

The above information shows the user's previous operation. Please generate next-step suggestions based on this context:
Suggestions must be highly relevant to the provided content
Suggestions should represent the most likely subsequent operations needed by most users

Requirements:
Output must strictly follow the example format using JSON
Output format must be a JSON array containing objects with "title" and "prompt" fields
Output must ONLY contain the JSON array - no comments, explanations, or other content
"title" field should be concise English phrases (≤7 characters)
"prompt" field must contain complete English instructions for better LLM output quality
Maximum 7 array elements

Example output:
[{{"title": "Add Comments", "prompt": "Generate comments for the following code"}}, {{"title": "Validate Parameters", "prompt": "Add parameter validation code to the following"}}]

Output:
"""
