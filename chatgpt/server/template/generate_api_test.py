#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Initial template for generating test points
INITIAL_API_TEST_POINT_PROMPT = r"""
## Instructions
You are an experienced API interface test engineer.
# Context #
Input API documentation content, mainly including interface name, interface URL, request parameter examples, and return parameter examples.
Test point design specifications:
 - Accurately understand the interface functionality, parameter descriptions and examples, and design test points based on interface functionality and parameter descriptions or examples.
 - Design test points only for parameters with clear constraints, covering normal scenarios and abnormal scenarios. If insufficient constraints are provided for a parameter, don't generate test points for that parameter. **Do not** add constraints to parameters on your own!!!
 - For each test point, **provide specific examples** placed within parentheses (). Examples should not merely describe abnormal situations!!!
 - Diversify abnormal test points. For example, when validating string legality, generate test points with various illegal characters in the string.
 - Cover common test areas, test range reference: {test_range}
# Goal #
Design interface test points according to the interface functionality and test design specifications.

# Format #
Return JSON data following the format in the "output example", including only test_params_description and test_points. The test_params_description value should describe the parameters being tested, with detailed explanations of regular expression rules; the test_points value should describe test points, with multiple test points separated by "\n".

## Chain-of-Thought example
### input
- Interface name
New product interface
- Interface URL
/api/dmp/product
- Interface request type
POST
- Interface request parameters
Body parameters:
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

Query parameters:
query_param="is_enable=true&product_id=9"
- Parameter descriptions
Body parameters:
    "admin_id": "Required, parameter type: string, parameter description: Product administrator ID, matches regular expression pattern: ^[1-9][0-9]{5,6}$, parameter example: 929629",
    "bg_code": "Required, parameter type: string, parameter description: BG code",
    "devops_product_ids": "Optional, parameter type: string, parameter description: Bound devops products, multiple selection, comma-separated",
    "handler": "Required, parameter type: string, parameter description: Product manager",
    "is_enable": "Required, parameter type: boolean, parameter description: Whether enabled, true/false, parameter example: true",
    "cell_phone": "Required, parameter type: string, parameter description: Mobile phone number, valid length is 11, parameter example: 13680201225",
    "mail": "Optional, parameter type: short, parameter description: Parent level, empty if no parent",
    "ip": "Required, parameter type: string, parameter description: IP address, parameter example: 127.0.0.0"
Query parameters:
    "is_enable": "Required, parameter type: boolean, parameter description: Whether enabled, true/false, parameter example: true",
    "product_id": "Required, parameter type: string, parameter description: Product ID, cannot be empty, parameter example: 9, maximum length: 200",

Parameters to test (generate cases focusing only on these parameters, using fixed values for other parameters):
    admin_id, ip, cell_phone, product_id

### output example
{
"test_params_description": {
"admin_id":"Product administrator ID, valid length is 6-7 digits, starting with a number between 1 and 9, followed by 5 to 6 digits, which must be numbers between 0 and 9."
"cell_phone": "Mobile phone number, valid length is 11",
"ip": "IP address, valid IPv4 address",
"product_id": "Product ID, cannot be empty"
},
"test_points": "1.Test normal interface parameter - admin_id length within reasonable range (length 6, example: 632589)\n2.Test abnormal interface parameter - admin_id length exceeds maximum (length 8, example: 47128635)\n3.Test abnormal interface parameter - admin_id doesn't match regex, first digit is 0 (059645)\n4.Test abnormal interface parameter - admin_id contains special characters (5!16_68) (examples should cover as many special characters as possible, inserted at different positions in the string)\n5.Test normal interface parameter - valid IP address (192.168.0.6)\n6.Test abnormal interface parameter - invalid IP address (255.255.255.256)\n7.Test normal interface parameter - 11-digit valid phone number (13680201225)\n8.Test abnormal interface parameter - 12-digit invalid phone number (136802012250)\n9.Test normal interface parameter - product_id length within reasonable range (12)\n10.Test abnormal interface parameter - product_id length exceeds maximum (length 201)"
}

## input
- Interface name
{api_name}
- Interface URL
{api_url}
- Interface request type
{api_request_type}
- Interface request parameters
Body parameters:
```python
body_param = {request_info}
```
Query parameters:
query_param="{url_param}"
- Request parameter descriptions
Body parameters:
{api_request_info_desc}
Query parameters:
{api_url_param_desc}
Parameters to test (generate test points focusing only on these parameters, using fixed values for other parameters; if parameter type is array, only focus on array capacity validity and array parameter type validity tests, no need to expand testing array parameters):
{waiting_test_param}

## output
""".strip()

# Initial template for generating test sets
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
- Interface name
New product interface
- Interface URL
/api/dmp/product
- Interface request type
POST
- Interface request parameters
Body parameters:
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

Query parameters:
query_param="is_enable=true&product_id=9"
- Parameter descriptions
Body parameters:
    "admin": "Required, parameter type: string, parameter description: Product administrator, multiple selection, comma-separated",
    "bg_code": "Required, parameter type: string, parameter description: BG code",
    "devops_product_ids": "Optional, parameter type: string, parameter description: Bound devops products, multiple selection, comma-separated",
    "handler": "Required, parameter type: string, parameter description: Product manager",
    "is_enable": "Required, parameter type: boolean, parameter description: Whether enabled, true/false, parameter example: true",
    "name": "Required, parameter type: string, parameter description: Product name, cannot be empty, maximum length 128, parameter example: devops",
    "parent_id": "Optional, parameter type: short, parameter description: Parent level, empty if no parent",
    "sort_number": "Required, parameter type: short, parameter description: Product sort number"
Query parameters:
    "is_enable": "Required, parameter type: boolean, parameter description: Whether enabled, true/false, parameter example: true",
    "product_id": "Required, parameter type: string, parameter description: Product ID, cannot be empty, parameter example: 9, maximum length: 50",

Test points:
    1.Test abnormal interface parameter - missing optional parameter parent_id
    2.Test abnormal interface parameter - parameter type incorrect, parent_id should be string
    3.Test abnormal interface parameter - product_id length is 51 (maximum length + 1)

### output
{
    "test_sets": [
        {
            "name": "Test abnormal interface parameter - missing optional parameter parent_id",
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
            "name": "Test abnormal interface parameter - parameter type incorrect, parent_id should be string",
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
            "name": "Test abnormal interface parameter - product_id length is 51 (maximum length + 1)",
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
- Interface name
{api_name}
- Interface URL
{api_url}
- Interface request type
{api_request_type}
- Interface request parameters
Body parameters:
```python
body_param = {request_info}
```
Query parameters:
query_param="{url_param}"
- Request parameter descriptions
Body parameters:
{api_request_info_desc}
Query parameters:
{api_url_param_desc}

Test points: (generate test sets only for the following test points)
{test_points}

## output
""".strip()

DEFAULT_PYTEST_CASE_TEMPLATE = """# {test_point_name}
from pytest_micro.wraps import tag, title, grpcmock

@tag(id='{testcase_id}', level="bvt")
@title("{test_point_name}")
def {test_case_title}(mock_api, http_service):
    '''Http mock case example'''
    mock_api.add('/inner/test1', code=200)
    mock_api.add('/inner/test2', code=400)
    json_body = {request_json}
    res = http_service.{request_type}('{api_url}', json=json_body)
    assert res.status_code == {status_code}, res.text
    print(res.text)
"""

DEFAULT_API_TEST_RANGE = [
    {
        "dimension": "Numeric type boundary value testing",
        "coverage": ["Maximum value", "Maximum value+1", "Minimum value", "Minimum value-1", "Middle value", "Empty value"],
        "data_types": ["integer", "number"],
        "ignore_scenarios": []
    },
    {
        "dimension": "String validity",
        "coverage": [
            "Parameter length at maximum value",
            "Parameter length at maximum value+1",
            "Special characters (characters not allowed: &|\"',%<>/\\)",
            "Scenario-specific (IP subnet, IP range, MAC validity, URL validity, domain validity, date validity, time validity, special character tests)",
            "Character diversity (full-width, half-width, upper/lowercase, Chinese/English mixed)"
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
        "dimension": "Capacity validity testing",
        "coverage": [
            "Arrays have capacity boundaries, e.g., minimum 1 item, maximum 30 items, verify boundary values 0,1,30,31"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    },
    {
        "dimension": "Optional and required field testing",
        "coverage": [
            "Required fields not fully provided",
            "Only required fields provided (verify if optional fields return default values)"
        ],
        "data_types": ["Array"],
        "ignore_scenarios": []
    }
]
