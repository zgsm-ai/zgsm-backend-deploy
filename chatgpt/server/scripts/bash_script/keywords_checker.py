#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/12 10:52
# @Author  : 苏德利16646
# @Contact : 16646@sangfor.com
# @File    : keywords_checker.py
# @Software: PyCharm
# @Project : chatgpt-server
# @Desc    : 关键字检查，检查关键字核心字段是否存在空或者无意义描述字段

import json
import requests
import time
import pandas as pd
from copy import deepcopy
import concurrent.futures

# 用于调试测试生成效果
# 1、当前方案效果

PROMPT_TEMPLATE = """
# 角色
您是一位经验丰富的关键字驱动测试专家。

## 相关知识
### 1、关键字驱动测试
关键字驱动测试（Keyword-Driven Testing）是一种自动化测试方法，它通过使用关键字来表示测试步骤和操作，从而实现测试用例的编写和执行。
关键字驱动测试的核心思想是将测试逻辑与测试数据分离，使得测试用例更加易读、易维护和易扩展。

关键字驱动测试的主要特点
可读性强：测试用例由一系列关键字组成，这些关键字通常是自然语言的描述，易于理解。
可重用性：关键字可以在多个测试用例中重复使用，减少了代码重复，提高了测试用例的可维护性。
分离测试逻辑和数据：测试逻辑通过关键字定义，而测试数据可以存储在外部文件（如 Excel、CSV）中，便于管理和修改。
易于扩展：可以通过添加新的关键字来扩展测试框架的功能。
关键字驱动测试的结构
关键字驱动测试通常包括以下几个部分：

关键字库：定义一组关键字，每个关键字对应一个具体的操作或步骤。
测试数据：存储测试用例所需的数据，通常保存在外部文件中。
测试用例：由一系列关键字和测试数据组成，描述具体的测试流程。
### 2、关键字细节和规范
1. 命名规范
简洁明了：关键字名称应简洁明了，能够准确描述其功能。例如，Open Browser 比 Start Web Browser 更简洁。
使用动词：关键字名称通常以动词开头，表示要执行的操作。例如，Click Button、Enter Text。
一致性：保持命名的一致性，避免同一操作使用不同的名称。例如，始终使用 Login 而不是有时用 Sign In。
2. 参数化
使用参数：关键字应支持参数化，以提高其灵活性和重用性。例如，Open Browser 可以接受 URL 和浏览器类型作为参数。
默认值：如果某些参数有常用的默认值，可以在关键字定义中设置默认值，以简化调用。
3. 文档化
添加注释：为每个关键字添加注释，说明其功能、参数和返回值。这有助于其他人理解和使用这些关键字。
4. 原子性
单一职责：每个关键字应只执行一个明确的操作，避免过于复杂。这样可以提高关键字的重用性和可维护性。
组合关键字：可以通过组合多个简单关键字来实现复杂操作。例如，Login 关键字可以由 Open Browser、Enter Username、Enter Password 和 Click Login Button 组成。
5. 错误处理
异常处理：在关键字中添加适当的异常处理，以确保在发生错误时能够提供有用的错误信息，并进行必要的清理操作。
返回值：关键字可以返回值，以便调用者根据返回值进行进一步的操作或判断。

## 任务
以下会以json数据格式提供一组或多组关键字，关键字中关键字段[name, desc, params, id, expect]，请分析关键字定义是否合理，如果不合理指出理由。

## 返回参数示例1
{{ "unreasonable_reason": "name为空，关键字段不能为空", "unreasonable_status": True}}
## 返回参数示例2
{{ "unreasonable_reason": "", "unreasonable_status": False}}

## 关键字参数
{keywords_json}

## 返回json格式结果
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
    # 定义表头信息
    columns = ["namespace", "keyword_id", "keyword_data", "check_status", "reason"]

    # 创建DataFrame
    df = pd.DataFrame(form_data, columns=columns)

    # 或者保存到CSV文件
    df.to_csv("check_keywords_json_output_process.csv", index=False)

    print("数据已成功保存到表格中。")


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
    # 获取所有叶子节点
    leaf_nodes = get_leaf_nodes(keywords_json)
    # print(keywords_json[0])
    # print(leaf_nodes[0])
    leaf_nodes = leaf_nodes
    print(len(leaf_nodes))
    data = []
    fail_id_list_raw = []
    fail_id_list = []
    # 1 并行执行，执行效率高
    # 并行执行
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        if fail_id_list_raw:
            # 用于失败重试场景
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
    # 2 串行执行，方便调试
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
