#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/24 15:57
# @Author  : 苏德利16646
# @Contact : 16646@sangfor.com
# @File    : generate_api_test.py
# @Software: PyCharm
# @Project : chatgpt-server
# @Desc    : 生成api测试prompt模板

# 生成测试点初始提问模板
INITIAL_API_TEST_POINT_PROMPT = r"""
## 指令
您是一个经验丰富的API接口测试工程师。
# 上下文 #
输入API文档内容，主要包括接口名称、接口url，请求参数示例，和返回参数示例。
测试点设计规范：
 - 准确了解接口功能、参数说明和示例，根据接口功能和参数说明或示例设计测试点。
 - 只需要针对有明确约束的参数生成测试点，测试点覆盖正常场景和异常场景。如果针对某参数提供的约束不足，不需要生成该参数的用例。**不要**自行对参数增加约束！！！
 - 每一个测试点**提供具体示例**，例子放在（）内部。例子不要仅仅给出对异常情况的描述！！！
 - 异常测试点的多样化。例如验证string的合法性时，应生成含有多种不同非法字符的string的测试点。
 - 覆盖公共测试范围，测试范围参考：{test_range}
# 目标 #
根据接口功能和测试设计规范设计接口的测试点。

# 格式 #
参考【output 示例】格式返回json数据，数据只包含test_params_description和test_points，test_params_description值为待测参数说明，正则表达式需要详细解释正则规则；test_points值为测试点描述，多个测试点之间使用"\n"进行分割。

## Chain-of-Thought example
### input
- 接口名称
新增产品接口
- 接口url
/api/dmp/product
- 接口请求类型
POST
- 接口请求参数
body参数：
body_param = {
    "admin": "",
    "bg_code": "",
    "devops_product_ids": "",
    "handler": "",
    "is_enable": 1,
    "name": "",
    "parent_id": 0,
    "sort_number": 0
}

query参数：
query_param="is_enable=true&product_id=9"
- 参数说明
body参数：
    "admin_id": "必填，参数类型：string，参数说明：产品管理员ID，符合正则表达式模式：^[1-9][0-9]{5,6}$,参数示例：929629",
    "bg_code": "必填，参数类型：string，参数说明：所属BG",
    "devops_product_ids": "非必填，参数类型：string，参数说明：绑定的devops产品，多选，逗号隔开",
    "handler": "必填，参数类型：string，参数说明：产品负责人",
    "is_enable": "必填，参数类型：boolean，参数说明：是否启用，true/false，参数示例：true",
    "cell_phone": "必填：参数类型：string，参数说明：手机号，合法长度为11，参数示例：13680201225",
    "mail": "非必填，参数类型：short，参数说明：所属父级，没有父级则为空",
    "ip": "必填，参数类型：string，参数说明：ip地址，参数示例：127.0.0.0"
query参数：
    "is_enable": "必填，参数类型：boolean，参数说明：是否启用，true/false，参数示例：true",
    "product_id": "必填：参数类型：string，参数说明：产品id，不能为空，参数示例：9，最大长度：200",

待测参数（生成用例仅关注此参数，其他参数使用固定值）：
    admin_id、ip、cell_phone、product_id

### output 示例
{
"test_params_description": {
"admin_id":"产品管理员ID，合法长度为6-7位，以1到9之间的数字开头，后面必须跟着5到6个数字，且这些数字必须是0到9之间的数字。"
"cell_phone": "手机号，合法长度为11",
"ip": "ip地址，合法的ipv4地址",
"product_id": "产品id，不能为空"
},
"test_points": "1.测试接口参数正常-admin_id长度在合理范围内（长度为6，例如632589）\n2.测试接口参数异常-admin_id长度为最大长度+1（长度为8，例如47128635）\n3.测试接口参数异常-admin_id不符合正则表达式，第一位为0（059645）\n4.测试接口参数异常-admin_id包含特殊字符（5!16_68）（这里的示例应该涵盖尽量多种特殊字符，并且插入在字符串的不同位置中）\n5.测试接口参数正常-ip为合法地址（192.168.0.6）\n6.测试接口参数异常-ip为非法地址（255.255.255.256）\n7.测试接口参数正常-cell_phone为11位合法手机号（13680201225）\n8.测试接口参数异常-cell_phone为12位非法号码（136802012250）\n9.测试接口参数正常-参数product_id长度在合理范围内（12）\n10.测试接口参数异常-参数product_id长度为最大长度+1（长度为201）"
}

## input
- 接口名称
{api_name}
- 接口url
{api_url}
- 接口请求类型
{api_request_type}
- 接口请求参数
body参数：
```python
body_param = {request_info}
```
query参数：
query_param="{url_param}"
- 请求参数说明
body参数：
{api_request_info_desc}
query参数：
{api_url_param_desc}
待测参数（生成测试点仅关注此参数，其他参数使用固定值，若参数类型为array则只关注array容量合法性和array参数类型合法性测试，不需要展开测试array里面参数）：
{waiting_test_param}

## output
""".strip()

# 生成测试集初始提问模板
INITIAL_API_TEST_SET_PROMPT = """
## Instructions
You are an experienced API interface testing engineer.
Background: Input the API content and input the interface information, mainly including the interface name,
the interface url, Request the parameter example, and return the parameter example.
Understand the interface function according to the interface information, test set for building API interfaces based
 on test points.
The test set shall include both the request parameters and the return parameters.
Your tasks can be summarized as follows:
- Accurately understand the interface functions, parameter usage and expected interface return.
- Build the test sets based on interface functions and parameters and test points.
Output is in json format.
When generating a string given its length L, output like this: "a*L"

## Chain-of-Thought example
### input
- 接口名称
新增产品接口
- 接口url
/api/dmp/product
- 接口请求类型
POST
- 接口请求参数
body参数：
body_param = {
    "admin": "",
    "bg_code": "",
    "devops_product_ids": "",
    "handler": "",
    "is_enable": 1,
    "name": "",
    "parent_id": 0,
    "sort_number": 0
}

query参数：
query_param="is_enable=true&product_id=9"
- 参数说明
body参数：
    "admin": "必填，参数类型：string，参数说明：产品管理员，多选，逗号隔开",
    "bg_code": "必填，参数类型：string，参数说明：所属BG",
    "devops_product_ids": "非必填，参数类型：string，参数说明：绑定的devops产品，多选，逗号隔开",
    "handler": "必填，参数类型：string，参数说明：产品负责人",
    "is_enable": "必填，参数类型：boolean，参数说明：是否启用，true/false，参数示例：true",
    "name": "必填：参数类型：string，参数说明：产品名，不能为空，最大长度128，参数示例：devops",
    "parent_id": "非必填，参数类型：short，参数说明：所属父级，没有父级则为空",
    "sort_number": "必填，参数类型：short，参数说明：产品排序号"
query参数：
    "is_enable": "必填，参数类型：boolean，参数说明：是否启用，true/false，参数示例：true",
    "product_id": "必填：参数类型：string，参数说明：产品id，不能为空，参数示例：9，最大长度：50",

测试点：
    1.测试接口参数异常-缺少非必填参数parent_id
    2.测试接口参数异常-参数值类型不对,parent_id应该为字符串
    3.测试接口参数异常-参数product_id长度为51（最大长度+1）

### output
{
    "test_sets": [
        {
            "name": "测试接口参数异常-缺少非必填参数parent_id",
            "test_case_title": "test_lack_unnecessary_param_parent_id_case",
            "input_body_param": {
                "admin": "sudeli",
                "bg_code": "test_bg",
                "devops_product_ids": "",
                "handler": "",
                "is_enable": 1,
                "name": "",
                "sort_number": 0,
                "product_id": "9"
            },
            "input_query_param": "is_enable=true&product_id=9",
            "output_status_code": 200
        },
        {
            "name": "测试接口参数异常-参数值类型不对,parent_id应该为字符串",
            "test_case_title"： "test_parent_id_wrong_param_type_case",
            "input_body_param": {
                "admin": "sudeli",
                "bg_code": "test_bg",
                "devops_product_ids": "",
                "handler": "",
                "is_enable": 1,
                "name": "",
                "parent_id": "test_id",
                "sort_number": 0,
                "product_id": "9"
            },
            "input_query_param": "is_enable=true&product_id=9",
            "output_status_code": 400
        },
        {
            "name": "测试接口参数异常-参数product_id长度为51（最大长度+1）",
            "test_case_title"： "test_parent_id_wrong_param_type_case",
            "input_body_param": {
                "admin": "sudeli",
                "bg_code": "test_bg",
                "devops_product_ids": "",
                "handler": "",
                "is_enable": 1,
                "name": "",
                "parent_id": "test_id",
                "sort_number": 0,
                "product_id": "a*51"
            },
            "input_query_param": "is_enable=true&product_id=9",
            "output_status_code": 400
        }
    ]
}

## input
- 接口名称
{api_name}
- 接口url
{api_url}
- 接口请求类型
{api_request_type}
- 接口请求参数
body参数：
```python
body_param = {request_info}
```
query参数：
query_param="{url_param}"
- 请求参数说明
body参数：
{api_request_info_desc}
query参数：
{api_url_param_desc}

测试点：（生成测试集仅针对以下测试点）
{test_points}

## output
""".strip()

DEFAULT_PYTEST_CASE_TEMPLATE = """# {test_point_name}
from pytest_micro.wraps import tag, title, grpcmock

@tag(id='{testcase_id}', level="bvt")
@title("{test_point_name}")
def {test_case_title}(mock_api, http_service):
    '''http mock的案例举例'''
    mock_api.add('/inner/test1', code=200)
    mock_api.add('/inner/test2', code=400)
    json_body = {request_json}
    res = http_service.{request_type}('{api_url}', json=json_body)
    assert res.status_code == {status_code}, res.text
    print(res.text)
"""

DEFAULT_API_TEST_RANGE = [
    {
        "dimension": "数字类型边界值测试",
        "coverage": ["最大值", "最大值+1", "最小值", "最小值-1", "中间值", "空值"],
        "data_types": ["integer", "number"],
        "ignore_scenarios": []
    },
    {
        "dimension": "字符串合法性",
        "coverage": [
            "参数长度为最大长度值",
            "测试参数长度为最大长度值+1",
            "特殊字符（特殊字符不能下发：&|\"',%<>/\\）",
            "具体场景相关（IP子网，IP范围，mac合法性，url合法性，域名合法性，日期合法性，时间合法性，特殊字符测试）",
            "字符多样性（全角，半角，大小写，中英文结合）"
        ],
        "data_types": ["string"],
        "ignore_scenarios": [
            "date",
            "time",
            "email",
            "ipv4",
            "ipv6",
            "uri",
            "hostname",
            "date-time"
        ]
    },
    {
        "dimension": "容量合法性测试",
        "coverage": [
            "数组是有容量边界的，比如最小允许1条，最大允许30条，那就要验证0,1,30,31 这些边界值"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    },
    {
        "dimension": "选填和必填测试",
        "coverage": [
            "必填携带不全",
            "只填写必填（需要验证选填返回的是否是默认值）"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    }
]
