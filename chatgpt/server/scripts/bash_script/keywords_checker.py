#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import time
import pandas as pd
from copy import deepcopy
import concurrent.futures

# For debugging and testing the generation effect
# 1. Current scheme effect

PROMPT_TEMPLATE = """
# Role
You are an experienced keyword-driven testing expert.

## Related Knowledge
### 1. Keyword-driven testing
Keyword-driven testing is an automation testing method that uses keywords to represent test steps and operations, enabling the writing and execution of test cases.
The core idea of keyword-driven testing is to separate test logic from test data, making test cases more readable, maintainable, and expandable.

Main features of keyword-driven testing:
High readability: Test cases consist of a series of keywords, which are typically natural language descriptions that are easy to understand.
Reusability: Keywords can be reused in multiple test cases, reducing code duplication and improving test case maintainability.
Separation of test logic and data: Test logic is defined through keywords, while test data can be stored in external files (such as Excel, CSV), making it easy to manage and modify.
Easy to extend: The test framework's functionality can be extended by adding new keywords.
Structure of keyword-driven testing
Keyword-driven testing typically includes the following parts:

Keyword library: Defines a set of keywords, with each keyword corresponding to a specific operation or step.
Test data: Stores the data needed for test cases, typically saved in external files.
Test cases: Composed of a series of keywords and test data, describing the specific test process.
### 2. Keyword details and specifications
1. Naming conventions
Concise and clear: Keyword names should be concise and clear, accurately describing their functionality. For example, "Open Browser" is more concise than "Start Web Browser".
Use verbs: Keyword names typically start with a verb, indicating the operation to be performed. For example, "Click Button", "Enter Text".
Consistency: Maintain naming consistency, avoid using different names for the same operation. For example, always use "Login" instead of sometimes using "Sign In".
2. Parameterization
Use parameters: Keywords should support parameterization to increase their flexibility and reusability. For example, "Open Browser" can accept URL and browser type as parameters.
Default values: If some parameters have commonly used default values, they can be set in the keyword definition to simplify calls.
3. Documentation
Add comments: Add comments to each keyword, explaining its functionality, parameters, and return values. This helps others understand and use these keywords.
4. Atomicity
Single responsibility: Each keyword should only perform one clear operation, avoiding excessive complexity. This can improve the reusability and maintainability of keywords.
Combined keywords: Complex operations can be achieved by combining multiple simple keywords. For example, the "Login" keyword can consist of "Open Browser", "Enter Username", "Enter Password", and "Click Login Button".
5. Error handling
Exception handling: Add appropriate exception handling in keywords to ensure that useful error information is provided when errors occur, and necessary cleanup operations are performed.
Return values: Keywords can return values to allow callers to perform further operations or judgments based on the return values.

## Task
The following will provide one or more keywords in JSON data format, with key fields in the keywords [name, desc, params, id, expect]. Please analyze whether the keyword definitions are reasonable, and if not, provide the reason.

## Return parameter example 1
{{ "unreasonable_reason": "name is empty, key fields cannot be empty", "unreasonable_status": True}}
## Return parameter example 2
{{ "unreasonable_reason": "", "unreasonable_status": False}}

## Keyword parameters
{keywords_json}

## Return JSON format result
"""

header = {"api-key": "MTU4MTU6cWlhbmxpdWFwaWtleTroi4/lvrfliKkxNjY0Njo5MDI3"}


def get_leaf_nodes(data, leaf_nodes=None):
    if leaf_nodes is None:
        leaf_nodes = []

    for item in data:
        if 'children' in item and item['children']:
            get_leaf_nodes(item['children'], leaf_nodes)
        else:
            leaf_nodes.append(item)

    return leaf_nodes


def check_keywords_json(keyword_json):
    keyword = deepcopy(keyword_json)
    for i in ['author', 'tags', 'example', 'namespace']:
        if i in keyword:
            keyword.pop(i)
    prompt = PROMPT_TEMPLATE.format(keywords_json=keyword)
    # print(f"prompt: {prompt}")

    ai_body = {
        "language": "vue",
        "code": "",
        "custom_instructions": "",
        "prompt": prompt,
        "action": "chat",
        "conversation_id": "",
        "stream": False,
        "collection_list": ["sase", "idux"],
        "git_path": "",
        "response_format": "json_object"
    }

    # ai_response = requests.post(url=ai_url, headers=header, json=ai_body)
    print("#---------------------------------- result -------------------------------")
    # print("#gpt3.5 result" + ai_response.json().get("model"))
    # print(ai_response.json().get("choices")[0].get("message").get("content"))

    header_gpt4 = {"api-key": "MTU4MTU6cWlhbmxpdWFwaWtleTroi4/lvrfliKkxNjY0Njo5MDI3", "cookie": "beta_keys=gpt-4",
                   "ide": "web",
                   "model": "GPT-4o",
                   "ide_version": "2.1.0",
                   "user-agent": "cicd service"
                   }
    cookies = {'beta_keys': 'gpt-4o'}

    # token_list = []
    # count = 2
    ai_url = "https://chatgpt.sangfor.com/api/v2/completion"
    print("")
    start = time.time()
    ai_response = requests.post(url=ai_url, headers=header_gpt4, json=ai_body, cookies=cookies)
    end = time.time()
    print(end - start)

    print(ai_response.text, ai_url)
    print("#gpt4o result: " + str(ai_response.json().get("model", "")) + " url: " + ai_url)
    # print(ai_response.json().get("choices")[0].get("message").get("content").lstrip("```json").rstrip("```").strip())
    # print(type(
    #     ai_response.json().get("choices")[0].get("message").get("content").lstrip("```json").rstrip("```").strip()))

    import json
    result_data = json.loads(
        ai_response.json().get("choices")[0].get("message").get("content").lstrip("```json").rstrip("```").strip())

    print(result_data)
    return result_data


def save_to_excel(form_data):
    # Define header information
    columns = ["namespace", "keyword_id", "keyword_data", "check_status", "reason"]

    # Create DataFrame
    df = pd.DataFrame(form_data, columns=columns)

    # Or save to CSV file
    df.to_csv("check_keywords_json_output_process.csv", index=False)

    print("Data has been successfully saved to the table.")


def process_node(index):
    try:
        print(f"node= {leaf_nodes[index]}")
        process_result = check_keywords_json(leaf_nodes[index])
    except Exception as e:
        print(f"i={index} xxxxxxxxxxxxxxxxxxx +++++++++ xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        fail_id_list.append(index)
        print(str(e))
        return []
    return [leaf_nodes[index]['namespace'], leaf_nodes[index]['id'], leaf_nodes[index],
            process_result['unreasonable_status'],
            process_result['unreasonable_reason']]


if __name__ == "__main__":
    with open(r'./keywords.2024.04.json', 'r', encoding='utf-8') as f:
        keywords_json = json.loads(f.read())
    # Get all leaf nodes
    leaf_nodes = get_leaf_nodes(keywords_json)
    # print(keywords_json[0])
    # print(leaf_nodes[0])
    leaf_nodes = leaf_nodes
    print(len(leaf_nodes))
    data = []
    fail_id_list_raw = []
    fail_id_list = []
    # 1 Parallel execution, higher execution efficiency
    # Parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        if fail_id_list_raw:
            # For failure retry scenarios
            future_to_node = {executor.submit(process_node, node_id): node_id for node_id in fail_id_list_raw}
        else:
            future_to_node = {executor.submit(process_node, node_id): node_id for node_id in range(len(leaf_nodes))}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_node)):
            try:
                result = future.result()
                data.append(result)
                print(f"i={i} len fail_id_list={len(fail_id_list)} ################ +++++++++ ################")
            except Exception as exc:
                print(f'Node {future_to_node[future]} generated an exception: {exc}')
    # 2 Serial execution, easier for debugging
    # for i in fail_id_list_raw:
    #     result = check_keywords_json(leaf_nodes[i])
    #     data.append([leaf_nodes[i]['namespace'], leaf_nodes[i]['id'], leaf_nodes[i], result['unreasonable_status'],
    #                  result['unreasonable_reason']])
    #     print(f"i={i} len fail_id_list={len(fail_id_list)} ################ +++++++++ ################")
    print("start save data to excel")
    save_to_excel(data)
    print(f"len data={len(data)}, len fail_id_list={len(fail_id_list)}")
    print(f"fail_id_list={fail_id_list}")

# print(token_list)
