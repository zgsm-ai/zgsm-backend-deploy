#!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate test point initial question template
INITIAL_API_TEST_POINT_PROMPT = r"""
## Instructions
You are an experienced API interface testing engineer.
# Context #
Input API documentation content, mainly including interface name, interface url, request parameter examples, and return parameter examples.
Test point design specifications:
 - Accurately understand the interface function, parameter descriptions, and examples, and design test points based on the interface function and parameter descriptions or examples.
 - Only generate test points for parameters with clear constraints, covering normal and abnormal scenarios. If insufficient constraints are provided for a parameter, do not generate test cases for that parameter. **Do not** add constraints to parameters yourself!!!
 - Each test point should **provide specific examples**, placed inside parentheses. Examples should not only describe abnormal situations!!!
 - Diversify abnormal test points. For example, when verifying the validity of a string, generate test points containing various different illegal characters.
 - Cover common test ranges, refer to the test range: {test_range}
# Target #
Design test points for the interface based on interface functions and test design specifications.

# Format #
Refer to the [output example] format to return JSON data, including test_params_description and test_points. The test_params_description value is the parameter description to be tested, and the regular expression needs to explain the regular rules in detail; the test_points value is the test point description, and multiple test points are separated by "\n".

## Chain-of-Thought example
### input
- Interface Name
Add Product Interface
- Interface URL
/api/dmp/product
- Interface Request Type
POST
- Interface Request Parameters
body parameters:
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

query parameters:
query_param="is_enable=true&product_id=9"
- Parameter Description
body parameters:
    "admin_id": "Required, Parameter Type: string, Parameter Description: Product administrator ID, matches the regular expression pattern: ^[1-9][0-9]{5,6}$, Parameter Example: 929629",
    "bg_code": "Required, Parameter Type: string, Parameter Description: BG to which it belongs",
    "devops_product_ids": "Optional, Parameter Type: string, Parameter Description: Bound devops products, multiple selections, separated by commas",
    "handler": "Required, Parameter Type: string, Parameter Description: Product负责人",
    "is_enable": "Required, Parameter Type: boolean, Parameter Description: Whether to enable, true/false, Parameter Example: true",
    "cell_phone": "Required: Parameter Type: string, Parameter Description: Cell phone number, valid length is 11, Parameter Example: 13680201225",
    "mail": "Optional, Parameter Type: short, Parameter Description: Parent level, empty if no parent level",
    "ip": "Required, Parameter Type: string, Parameter Description: ip address, Parameter Example: 127.0.0.0"
query parameters:
    "is_enable": "Required, Parameter Type: boolean, Parameter Description: Whether to enable, true/false, Parameter Example: true",
    "product_id": "Required: Parameter Type: string, Parameter Description: Product ID, cannot be empty, Parameter Example: 9, Maximum Length: 200",

Parameters to be tested (generate test cases only focus on this parameter, other parameters use fixed values):
    admin_id, ip, cell_phone, product_id

### output example
{
"test_params_description": {
"admin_id":"Product administrator ID, valid length is 6-7 digits, starting with a digit between 1 and 9, followed by 5 to 6 digits, and these digits must be between 0 and 9."
"cell_phone": "Cell phone number, valid length is 11",
"ip": "ip address, valid ipv4 address",
"product_id": "Product ID, cannot be empty"
},
"test_points": "1. Test interface parameter normal - admin_id length is within a reasonable range (length is 6, e.g. 632589)\n2. Test interface parameter abnormal - admin_id length is maximum length + 1 (length is 8, e.g. 47128635)\n3. Test interface parameter abnormal - admin_id does not conform to the regular expression, first digit is 0 (059645)\n4. Test interface parameter abnormal - admin_id contains special characters (5!16_68) (This example should cover as many special characters as possible and insert them in different positions in the string)\n5. Test interface parameter normal - ip is a valid address (192.168.0.6)\n6. Test interface parameter abnormal - ip is an invalid address (255.255.255.256)\n7. Test interface parameter normal - cell_phone is a 11-digit valid cell phone number (13680201225)\n8. Test interface parameter abnormal - cell_phone is a 12-digit invalid number (136802012250)\n9. Test interface parameter normal - parameter product_id length is within a reasonable range (12)\n10. Test interface parameter abnormal - parameter product_id length is maximum length + 1 (length is 201)"
}

## input
- Interface Name
{api_name}
- Interface URL
{api_url}
- Interface Request Type
{api_request_type}
- Interface Request Parameters
body parameters:
```python
body_param = {request_info}
```
query parameters:
query_param="{url_param}"
- Request Parameter Description
body parameters:
{api_request_info_desc}
query parameters:
{api_url_param_desc}
Parameters to be tested (generate test points only focus on this parameter, other parameters use fixed values. If the parameter type is array, only focus on array capacity validity and array parameter type validity test, do not expand to test parameters inside the array):
{waiting_test_param}

## output
""".strip()

# generate test set initial question template
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
Add Product Interface
- 接口url
/api/dmp/product
- 接口请求类型
POST
- Interface Request Parameters
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

query parameters:
query_param="is_enable=true&product_id=9"
- Parameter Description
body parameters:
    "admin": "Required, Parameter Type: string, Parameter Description: Product administrator, multiple selections, separated by commas",
    "bg_code": "Required, Parameter Type: string, Parameter Description: BG to which it belongs",
    "devops_product_ids": "Optional, Parameter Type: string, Parameter Description: Bound devops products, multiple selections, separated by commas",
    "handler": "Required, Parameter Type: string, Parameter Description: Product负责人",
    "is_enable": "Required, Parameter Type: boolean, Parameter Description: Whether to enable, true/false, Parameter Example: true",
    "name": "Required: Parameter Type: string, Parameter Description: Product name, cannot be empty, maximum length 128, Parameter Example: devops",
    "parent_id": "Optional, Parameter Type: short, Parameter Description: Parent level, empty if no parent level",
    "sort_number": "Required, Parameter Type: short, Parameter Description: Product sort number"
query parameters:
    "is_enable": "Required, Parameter Type: boolean, Parameter Description: Whether to enable, true/false, Parameter Example: true",
    "product_id": "Required: Parameter Type: string, Parameter Description: Product ID, cannot be empty, Parameter Example: 9, Maximum Length: 50",

Test points:
    1.Test interface parameter abnormal - missing optional parameter parent_id
    2.Test interface parameter abnormal - parameter value type is incorrect, parent_id should be a string
    3.Test interface parameter abnormal - parameter product_id length is 51 (maximum length + 1)

### output
{
    "test_sets": [
        {
            "name": "Test interface parameter abnormal - missing optional parameter parent_id",
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
            "name": "Test interface parameter abnormal - parameter value type is incorrect, parent_id should be a string",
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
            "name": "Test interface parameter abnormal - parameter product_id length is 51 (maximum length + 1)",
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
- Interface Name
{api_name}
- Interface URL
{api_url}
- Interface Request Type
{api_request_type}
- Interface Request Parameters
body parameters:
```python
body_param = {request_info}
```
query parameters:
query_param="{url_param}"
- Request Parameter Description
body parameters:
{api_request_info_desc}
query parameters:
{api_url_param_desc}

Test points: (Generate test sets only for the following test points)
{test_points}

## output
""".strip()

DEFAULT_PYTEST_CASE_TEMPLATE = """# {test_point_name}
from pytest_micro.wraps import tag, title, grpcmock

@tag(id='{testcase_id}', level="bvt")
@title("{test_point_name}")
def {test_case_title}(mock_api, http_service):
    '''http mock example'''
    mock_api.add('/inner/test1', code=200)
    mock_api.add('/inner/test2', code=400)
    json_body = {request_json}
    res = http_service.{request_type}('{api_url}', json=json_body)
    assert res.status_code == {status_code}, res.text
    print(res.text)
"""

DEFAULT_API_TEST_RANGE = [
    {
        "dimension": "Numeric type boundary value test",
        "coverage": ["Maximum value", "Maximum value + 1", "Minimum value", "Minimum value - 1", "Middle value", "Null value"],
        "data_types": ["integer", "number"],
        "ignore_scenarios": []
    },
    {
        "dimension": "String validity",
        "coverage": [
            "Parameter length is the maximum length value",
            "Test parameter length is the maximum length value + 1",
            "Special characters (special characters cannot be issued: &|\"',%<>/\\)",
            "Specific scenario related (IP subnet, IP range, mac validity, url validity, domain name validity, date validity, time validity, special character test)",
            "Character diversity (full-width, half-width, uppercase, lowercase, Chinese and English combination)"
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
        "dimension": "Capacity validity test",
        "coverage": [
            "The array has capacity boundaries, such as a minimum of 1 and a maximum of 30, so you need to verify these boundary values: 0, 1, 30, 31"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    },
    {
        "dimension": "Optional and required test",
        "coverage": [
            "Required not fully carried",
            "Only fill in the required (need to verify whether the optional return is the default value)"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    }
]
