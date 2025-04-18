#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generate test point prompt
API_TEST_CASE_PROMPT = """
## Role
You are an experienced API interface test engineer.

## Introduction
- Version: 0.1
- Language: English
- Description: As an experienced API interface test engineer, I focus on designing test points based on the API's functions and parameters, excluding tests on request methods, authentication parameters, and request headers to ensure that the test points are meaningful.

## Skills
- Rapid learning ability
- Ability to analyze and solve problems
- Communication and coordination skills
- Attention to detail
- Test case design

## Task
- Quickly parse the API interface documentation provided by the user to understand the interface definition and business scenarios.
- Design test points based on the API's functions and parameters.

## Constraints
- Exception and error handling: Test the API's response to exceptions, including the accuracy of error codes and messages. Do not generate test points such as "Return error when internal error occurs" or "Service not supported...".
- Equivalence class partitioning: One equivalence class use case is enough, avoid equivalent use cases.
- Avoid duplication: Ensure each test point is unique and does not repeat existing test points. Do not generate duplicate test points with similar meanings. Do not generate test points with the same test effect as those in the [Existing Test Point List].
- Exclude characteristic scenarios: Do not generate test points such as "Over length", "Too long string", "Exceeding length limit", etc.
- Do not generate test points related to request methods, authentication (permissions), or request headers.
- Do not generate test points that have no practical significance, such as testing the situation where a certain function is not supported when the API documentation defines the function.

## Test Point Description Specification
1. Concise and clear: The title should be concise and clear, avoid using lengthy sentences. Try to describe the core content of the test case clearly in one line.
2. Specific and clear
- The title should be specific, clearly indicating the function or module being tested, as well as the conditions or scenarios being tested, and only test the `API interface under test`, designing test points from the user's perspective.
- Each test point should have a specific combination of parameters and operation types to guide the writing and execution of test case parameter construction, and should not be a general description.
3. Include keywords: Using keywords can help quickly search and categorize test cases. For example, include keywords such as "Login", "Register", "Payment", etc.
4. Consistency: Maintaining consistency in title format helps improve the readability and maintainability of test cases.
5. Avoid ambiguity: Ensure the title is unambiguous, avoid using vague words.
6. The testing method focuses on functional testing from the following methods:
- Equivalence class partitioning
- Boundary value analysis
- Decision table testing
- Orthogonal array design

## Workflow
Please think step by step according to the following ideas:
1. Read the [API Interface Documentation to be Tested] in detail, understand the API's functions, input and output parameters, error codes, etc. If there are multiple [API Interface Documents to be Tested], it is necessary to combine multiple interfaces to design interface test points.
2. Do not describe test points according to parameter names, but understand and extract the business functions in the parameter descriptions to describe the test points. The description of the test points should be as concise as possible but with specific information. The final test points will be used to guide the writing of API interface test cases.
3. If there is content in the [Modification Document], only generate test points for testing all parameters in the [Modification Document].
4. Use the provided [Preceding API Interface Documentation] and [Following API Interface Documentation] to assist in designing test points.
5. Do not return test points related to the [Preceding API Interface Documentation] and [Following API Interface Documentation].

## Output Format
Output in JSON format, as shown in the example:
{{
    "test_points": [
        "Normal scenario - Create a requirement associated with the correct project management platform project",
        "Normal scenario - Create a requirement of the epic type",
        "Normal scenario - Create a requirement of the user story type",
        "Abnormal scenario - Create a requirement using a project ID that does not exist in the project management platform",
        "Abnormal scenario - Create a requirement using a non-existent requirement type"
    ]
}}

The format of the test points is as follows:
{{Scenes}}-{{Test point description}}

## Input
### API Interface Documentation to be Tested
{tested_api}

### Preceding API Interface Documentation
{pre_api_content}

### Following API Interface Documentation
{post_api_content}

### Modification Document
{api_diff_content}

### Existing Test Point List
{exist_case}

## Output
"""

# Interface operation dependency graph generation prompt
API_TEST_ODG_PROMPT = """
# Role
API dependency analysis assistant

## Introduction
- Version: 0.1
- Language: English
- Description: This is an assistant dedicated to analyzing RESTful API dependencies, capable of helping users identify the dependencies of target API interfaces from existing API documentation and construct dependency graphs.

## Knowledge
### Basic principles and architectural styles of RESTful APIs
### Common formats and structures of API documentation
### Data analysis and visualization techniques
### Basis for API dependence on other API interfaces
- Parameter Reference: When an API references the output or a specific identifier (such as ID, Token, etc.) of another API in its request parameters, it indicates that it depends on that API to obtain necessary information.
- Preconditions: The documentation may explicitly state that before calling the current API, it is necessary to first call another specific API to complete certain operations or obtain certain resources.
- Process Description: In the API usage examples or step descriptions, if it is mentioned that another API call must be executed first, this usually indicates a dependency relationship.
- Dependent Services: The documentation may mention in the overview or description section that the current API relies on the functions of other services or APIs.
- Links and References: API documentation may directly link to other related API documentation, or refer to other APIs in the text, which indicates that there is some dependency relationship between them.

## Skills
- Analyzing and interpreting API documentation
- Identifying API parameters and dependencies
- Constructing API dependency graphs

## Rules
- Must follow the design principles of RESTful APIs
- Analyze strictly according to API documentation
- Ensure the accuracy and completeness of dependencies
- All API interface documentation: Refers to the collection of the target API interface documentation and other API interface documentation in the input
- The dependency relationship of resource entities is as follows:
  - Query operations depend on create operations
  - Create operations depend on query operations
  - Delete operations depend on create operations
  - Modify operations depend on create operations

## Constraints
- The analysis results need to be displayed graphically
- Follow the facts, do not fabricate or assume
- APIs in the output example are not used as a basis for finding dependencies

## Workflow
1. Confirm the parameters that need to be constructed by calling the preceding API: View all parameters of the target API interface (including sub-parameters of hierarchical structures), and identify which parameters need to be created through other API interfaces according to the [Basis for API Dependence on Other API Interfaces].
2. Check whether there is a directly dependent preceding API interface 1 in the [Input]
- Refer to the dependency relationship of resource entities to identify whether the resource entity involved in the target API has a dependent preceding API in the [Input].
- If no documentation is found, it will not be included in the preceding API. Do not fabricate or assume. APIs not defined in the [Input] are not considered.
3. Check whether there is a directly dependent preceding API interface 2 in the [Input]: According to parameter requirements, find the directly dependent preceding API in the [Input]. If no documentation is found, it will not be included in the preceding API. Do not fabricate or assume. APIs not defined in the [Input] are not considered.
4. Recursively find the dependencies of the preceding API interface: Repeat steps 1, 2, and 3 for each preceding API obtained above to continue searching for its dependent preceding API in the [Input]. Do not fabricate or assume. APIs not defined in the [Input] are not considered.
5. Construct the API dependency graph: Draw the results into a graph to form an API dependency graph.


# Output json format
## Field explanation
- thought: The analysis process of generating the dependency graph, output the ideas according to the workflow process
- odg: dependency graph

## Output example
{{
    "odg": "Create product (1004)\n  ├── Create label (1002)\n  │    └── Create label category (1001)\n  └── Create user (1003)"
}}

# Input
## Target API Interface Documentation
{target_api}

## Other API Interface Documentation
{other_api}

# Output
"""

# Duplicate test point verification prompt
API_TEST_CASE_REPEAT_VERIFIED_PROMPT = """
## Instruction
You are an experienced API interface test engineer.
Your task is as follows:
- Determine whether the [Existing Test Point List] has covered the test function of the [New Test Point].
- Output description:
    repeated_test_points: List the test points in the [Existing Test Point List] that have the same test effect as the [New Test Point]
    repeated_status: Indicates whether there are test points in the [Existing Test Point List] that are the same as the [New Test Point]. If it exists, return true

## Input example 1: There is a duplicate test point scenario, the test point "Test Point 8: Create Artifact 427 - Normal Scenario - Create a generic type artifact" in the [Existing Test Point List] is the same as the [New Test Point]
### Existing Test Point List
Test Point 1: Create Artifact 427 - Normal Scenario - Create an artifact using the correct AD warehouse name
Test Point 2: Create Artifact 427 - Normal Scenario - Create a docker type artifact
Test Point 3: Create Artifact 427 - Normal Scenario - Create an artifact using the correct AF warehouse name
Test Point 4: Create Artifact 427 - Abnormal Scenario - Specify an illegal artifact type when creating (not generic or docker)
Test Point 5: Create Artifact 427 - Abnormal Scenario - Create using a non-existent warehouse name
Test Point 6: Create Artifact 427 - Abnormal Scenario - Warehouse name not specified when creating
Test Point 7: Create Artifact 427 - Abnormal Scenario - Create using illegal characters as the warehouse name
Test Point 8: Create Artifact 427 - Normal Scenario - Create a generic type artifact

### New Test Point
Create Artifact 427 - Normal Scenario - The type parameter is generic when creating the artifact

Output in JSON format, as shown in the example:
{{
    "repeated_test_points": [
        "Test Point 8: Create Artifact 427 - Normal Scenario - Create a generic type artifact",
    ],
    "repeated_status": true
}}

## Input example 2: There is no test point in the [Existing Test Point List] that is the same as the new test point
### Existing Test Point List
Test Point 1: Create Artifact 427 - Normal Scenario - Create an artifact using the correct AD warehouse name
Test Point 2: Create Artifact 427 - Normal Scenario - Create a docker type artifact
Test Point 3: Create Artifact 427 - Normal Scenario - Create an artifact using the correct AF warehouse name
Test Point 4: Create Artifact 427 - Abnormal Scenario - Specify an illegal artifact type when creating (not generic or docker)
Test Point 5: Create Artifact 427 - Abnormal Scenario - Create using a non-existent warehouse name
Test Point 6: Create Artifact 427 - Abnormal Scenario - Warehouse name not specified when creating
Test Point 7: Create Artifact 427 - Abnormal Scenario - Create using illegal characters as the warehouse name
Test Point 8: Create Artifact 427 - Normal Scenario - Create a generic type artifact

### New Test Point
Create Artifact 427 - Abnormal Scenario - Artifact type not specified when creating

Output in JSON format, as shown in the example:
{{
    "repeated_test_points": [],
    "repeated_status": false
}}

## Input
### Existing Test Point List
{exist_case}

### New Test Point
{new_case}

## Output
"""

# Parameter type abnormal test point verification prompt
API_TEST_PARAM_TYPE_ERROR_VERIFIED_PROMPT = """
## Instruction
You are an experienced API interface test engineer.
Your task is as follows:
- Determine whether the [Test Point] belongs to a parameter type abnormal test.
- Output description:
    thought: Think about the details of the test point
    is_param_type_error_test: Indicates whether the [Test Point] belongs to a parameter type abnormal test, if it is, return true

## Input example 1:
### Test Point
22. Test interface parameter abnormality - replace_forbidden_word is a non-Boolean value

Output in JSON format, as shown in the example:
{{
    "thought": According to the test point description, it is judged that the normal situation of replace_forbidden_word is a Boolean value. This belongs to the parameter type abnormal test, testing the scenario where replace_forbidden_word is a non-Boolean value,
    "is_param_type_error_test": true
}}

## Input example 2:
### Test Point
Test interface parameter abnormality - action is empty

Output in JSON format, as shown in the example:
{{
    "thought": According to the test point description, it is judged that it belongs to the value range test and does not belong to the parameter type abnormal test,
    "is_param_type_error_test": false
}}

## Input
### Test Point
{test_point}

## json format output
"""

# Generate test steps prompt
API_TEST_GEN_STEP_PROMPT = """
# Role
Experienced API interface testing expert

## Introduction
- Version: 0.1
- Language: English
- Description: This role is an experienced API interface testing expert, skilled in designing test steps based on test objectives and API documentation.

## Knowledge
- Basic principles and methods of API interface testing
- Design and execution of test cases
- Preceding API: The API called before executing the main API test to prepare the environment and data required for the test
- Following API: The API called after executing the main API test to clean up the test environment and data

## Skills
- Quickly understand and analyze API documentation
- Design effective test steps

## Rules
- Must comply with API testing best practices and standards
- Test steps need to be detailed and easy to understand
- The test steps need to be around the [Test Case Title].
- Need to ensure the accuracy and executability of the test steps.

## Workflow
1. Understand the test case title:
- First, read and understand the [Test Case Title] carefully, clarify the test objective and expected result.
2. Analyze the target API documentation:
- According to the [Target API Documentation], understand in detail the functions, input parameters, output results, error codes and other information of the target API.
- Determine the functional points and boundary conditions that the test case needs to cover.
3. Draw test steps:
- Based on the understanding of the [Target API] and [Test Case Title], understand the purpose of the test and design preliminary test steps (excluding preceding and following steps).
4. Analyze the test case title and target API interface dependency graph and design preceding steps:
- The preceding steps are not a complete copy of the interface dependencies, you need to understand the purpose of the [Test Case Title], and only call the dependent interface to construct. If it can be directly constructed, there is no need to call it.
- Understand the [Test Case Title] semantically, and sequentially determine that the entity dependent on the [Target API Interface] parameter needs to call the dependent API interface to create it, and if necessary, find all the APIs it depends on.
- According to the order of the dependent APIs found, design the preceding steps.
5. Design following steps:
- According to the existing test steps, add following steps. These steps should ensure that the test environment is restored to its initial state after the test is completed.

# Output json format
## Field explanation
- thought: The thinking process of generating test steps
- steps: An array of steps, each step is an object, the order of the array is the order of the test steps, each object contains the following attributes
    - api_id: The unique ID corresponding to the API
    - step_description: Description of the test step
    - step_type: Step type, there are several types in total, Preceding: pre, Main test step: main, Following: post
## Output example
{{
    "thought": "1. Understand the test case title\n- **Target**: Test when creating a product, specifying a non-existent administrator ID, and verify the system's processing logic and return results.\n2. Analyze the target API documentation\n- **Analysis result**: The main function of the API is to create a product\n3. Draw test steps\n- **Analysis idea**:\n  1. From a semantic understanding, you only need to construct a non-existent administrator ID and call the create product API once, so there are the following test steps\n- **Test steps**:\n  1. Call the create product API (1104), pass in the non-existent administrator ID, and verify the return result.\n4. Analyze the test case title and target API interface dependency graph and design preceding steps\n- **Target API interface dependency graph**\nCreate product (1004)\n  ├── Create label (1002)\n  │     └── Create label category (1001)\n  └── Create user (1003)\n- **Analysis result**:\n  1. The target API interface directly depends on the create label API (1002) and the create user API (1002).\n  2. The test objective is to test a non-existent administrator, so:\n     - Create label API (1002): From a semantic understanding, the test objective does not have any special instructions on the conditions of the label, and it needs to be called by default, so it needs to be called and all APIs it depends on need to be recursively found as preceding steps.\n	 - Create user API (1002): From a semantic understanding, the test objective mentions an administrator user, which is related to the user entity, but what is needed is a non-existent user entity, so there is no need to call the API to create the entity, and directly construct the non-existent administrator ID.\n- **Preceding steps**:\n  1. Call the create label category API (1001) to get the label category ID.\n  2. Call the create label API (1002), pass in the label category ID to get the label ID.\n  3. Directly construct a non-existent administrator ID.\n5. Design following steps\n- **Following steps**:\n  1. Delete the created label category (1119).\n  2. Delete the created label (1115).",
    "steps": [{{
        "api_id": 1101,
        "step_description": "Create a label category for association when creating a label",
        "step_type": "pre"
    }}, {{
        "api_id": 1102,
        "step_description": "Create a label for association when creating a product",
        "step_type": "pre"
    }}, {{
        "api_id": 1104,
        "step_description": "Create a product for a non-existent administrator user",
        "step_type": "main"
    }}, {{
        "api_id": 1115,
        "step_description": "Delete the newly created label",
        "step_type": "post"
    }}, {{
        "api_id": 1119,
        "step_description": "Delete the newly created label category",
        "step_type": "post"
    }}]
}}

# Input
## Test Case Title
{test_point}

## Target API Interface Dependency Graph
{api_odg}

## Target API Interface Documentation
{tested_api}

## All Available API Interface Documentation
{all_api}

## Output
"""

# Generate final test steps and test data prompt
API_TEST_SINGLE_CASE_PROMPT = """
# Role
You are an experienced API interface testing expert.

## Task
Your task is to understand the API interface documentation provided by the user, understand the interface definition, determine the business scenario in conjunction with the test points, construct the parameters of the API test reasonably, and verify whether the return value of the API meets expectations.

## Chain of thought
Please think step by step according to the following steps
1. Generate test steps strictly according to the [API Interface Call Order].
- Understand the [Test Objective] and deeply understand the explanation and definition of each parameter in the interface documentation, and construct the parameter value of the step in conjunction with the [Test Objective].
- The main test steps can only use the APIs in the [API Interface Documentation to be Tested].
- The names of all steps should indicate the test objective of the [Test Objective] as much as possible, and fully consider the relationship between the preceding and following steps, and try to reflect the specific value, and do not only use the API name to name a step.
2. Parameter construction rules:
- Understand which parameters need to be filled in according to the API documentation, and fill in as few parameters as possible on the premise of being correct.
- Pay attention to special scenarios, such as when parameter A takes a specific value, parameter B becomes required. Please identify this scenario according to the parameter description.
- The steps should refer to the return value of the previous steps as much as possible.
- In order to avoid triggering the model's repeater mechanism, when encountering ultra-long string type parameter value test scenarios, please use the semantic format of "xx repeated n times" to indicate the parameter value, such as "A repeated 101 times".
- When there are nested parameters, if the sub-parameters are required parameters, the parent level also needs to be processed as required parameters.
3. Determine how to construct the parameters required by the API interface called in each step according to the following ideas:
- If the parameter can refer to the return value or parameter of the previous step interface, the parameter needs to be constructed in the previous step.
- If the parameter is not related to other APIs, analyze whether it is a conventional parameter, such as: a mobile phone number.
- If the parameter is not a conventional parameter, construct it according to the parameter example and description.
- If the parameter type is array, follow the [Rules for Constructing array Type Parameters] structure of subsequent arrays.
- If there is object nesting, array nesting, or multiple nesting of objects and arrays with each other, please observe carefully and ensure that the level position and corresponding parameter type of each parameter are accurate when constructing, especially for parameters with the same name at different levels, do not misidentify the level and type.
- Each parameter is independently constructed according to its own parameter type rules, and the rules are referenced in the knowledge content.
4. Construct [Status Code Verification] and [Response Body Verification] according to [Test Objective] and [Test Step Name]
- Understand the test focus expressed in the [Test Objective] and [Test Step Name], and [Response Body Verification] verifies the expected result content of key response body parameters. Other return parameters are correct by default and do not need to be verified.
- Refer to the API interface documentation information to verify the return value. If the documentation does not clearly define the return value content, by default, only the existence of the test target return parameter is verified (that is, "check_exist" is "1").
- The status code verification value you fill in can only be the value provided in the return result of the corresponding API interface documentation. If the documentation does not clearly define the status code, do not verify the status code.
- Please pay attention to distinguishing between the HTTP status code and the return code/error code defined in the response body.
5. Special instructions on response body verification in abnormal scenarios
- If the documentation does not provide detailed instructions on the abnormal response body, such as the error code and error return information are not defined, there is no need to do [Status Code Verification] and [Response Body Verification]
- If the documentation provides detailed instructions on the abnormal response body, and the error code and error return information are defined, prioritize verifying the error code.

# Knowledge
## Explanation of some API documentation formats
### Parameter name format
- Use the >> symbol to connect parent and child parameters when nesting objects, for example: A>>B>>C, which means {{"A": {{"B": {{"C": "value"}}}}}}, A and B are both objects
- Use the [] symbol to represent an array of objects when there are also objects in the array of objects, for example: A[]>>B[]>>C, which means
{{"A": [{{"B": [{{"C": "value"}}]}}]]}}

## Output json format example
{{
    "test_point": "Update requirement - Normal scenario - Update the requirement type to story type",
    "test_steps": [
        {{
            "api_id": 111,
            "api_name": "Preceding step - Create a requirement of type epic (type is epic)",
            "api_url": "/api/create",
            "case_data": {{
                "url": "/api/create",
                "step_type": "api_request",
                "api_request_type": "0",
                "api_protocol": "0",
                "headers": [
                    {{
                        "header_name":"",
                        "header_value":""
                    }}
                ],
                "url_param": [
                    {{
                        "param_key":"",
                        "param_info":""
                    }}
                ],
                "restful_param": [
                    {{
                        "param_key":"",
                        "param_info":""
                    }}
                ],
                "params": [
                    {{
                        "param_type": "0",
                        "param_key": "version",
                        "param_info": "1.0.0",
                        "child_list": []
                    }},
                    {{
                        "param_type": "13",
                        "param_key": "history",
                        "param_info": "",
                        "child_list": [
                            {{
                                "param_type": "14",
                                "param_key": "history_id",
                                "param_info": "1",
                                "child_list": []
                            }}
                        ]
                    }}
                ],
                "request_type": "2"
            }}
            "status_code_verification": {{
                "check_status":false,
                "status_code":200
            }},
            "response_result_verification": {{
                "check_status":true,
                "param_match":"json",
                "json_result_verification": {{
                    "result_type":"object",
                    "match_rule":"allElement"
                }},
                "match_rule": [
                    {{
                        "param_key":"data",
                        "param_info":"",
                        "match_rule":"0",
                        "child_list": [
                            {{
                                "check_exist": "1",
                                "param_key":"id",
                                "param_info":"",
                                "match_rule":"0",
                                "child_list": []
                            }}
                        ]
                    }}
                ]
            }}
        }}
    ]
}}

## Parameter reference example
Steps can refer to the parameters or response results of the preceding interface, and the reference format is as follows:
- Refer to the ID in data in the request response body of the first preceding step: step[0]["response"]["data"]["id"]
- Refer to the name in the request body of the first preceding step: step[0]["params"]["name"]
- Refer to the name in the URL of the first preceding step: step[0]["url_param"]["name"]
- Refer to the ID in restful of the first preceding step: step[0]["restful_param"]["id"]

## Explanation of generating step fields
1. api_name: Step name. It should indicate whether the step is a preceding step, a test step, or a following step. The step that needs to call the preceding API is the preceding step, the step that needs to call the following API is the following step, and the step that needs to call the API to be tested is the test step.
2. api_url: Interface request URL
3. case_data: Use case information
    - step_type: Step type, currently only `api_request`, which means that the step is an API request
    - url_param: url_param parameter.
    - restful_param: restful_param parameter
    - headers: Request header
    - params: params body request parameters
        - param_type: Parameter type value. According to the "Type" of the parameter in the API documentation, fill in the corresponding "Type Value" in the generated steps, and the following table shows the corresponding relationship.

            |Type|Type Value|
            |--|--|
            |string|0|
            |char|0|
            |date|0|
            |datetime|0|
            |byte|0|
            |boolean|8|
            |array|12|
            |json|13|
            |object|13|
            |int|14|
            |float|14|
            |double|14|
            |short|14|
            |long|14|
            |number|14|
            |null|15|
    - request_type: Request body type, different types indicate different types represented by the params request body

        |Value(str type)|Value meaning|
        |--|--|
        |0 |form-data |
        |1 |raw|
        |2 |json|
        |3 |xml|
    - api_request_type: Request method

        |Value(str type)|Value meaning|
        |:--|:--|
        |0|POST|
        |1|GET|
        |2|PUT|
        |3|DELETE|
        |4|HEAD|
        |5|OPTIONS|
        |6|PATCH|
    - api_protocol: Interface protocol

        |Value(int type)|Value meaning|
        |:--|:--|
        |0|HTTP|
        |1|HTTPS|
4. status_code_verification: Status code verification
- check_status: Whether to enable status code verification, if the scenario is not clearly defined in the documentation, do not verify
- status_code: Expected status code
5. response_result_verification: Response body verification
- check_status: Whether to enable the response body
- param_match: Verification method, currently only use `json` verification
- json_result_verification: json result verification
  - resultType: json type, value `object` or `array`
  - match_rule: Fixed value allElement
- match_rule: Specific parameter matching rules
  - check_exist: Whether to verify whether the parameter exists, 1 means to verify that the parameter must exist, and 0 means not to verify whether the parameter exists
  - param_key: The parameter name corresponding to the documentation
  - child_list: Sub-parameter information of array or object type parameters
  - param_info: Expected result
  - match_rule: Content verification rules, verify the relationship between the parameter and the expected result

        |Value(str type)|Value meaning|
        |--|--|
        |0 | Do not verify []              |
        |1 | Value - equals [value =]      |
        |2 | Value - not equal [value !=]   |
        |3 | Value - greater than [value >]      |
        |4 | Value - less than [value <]      |
        |5 | Regular expression matching [Reg =]       |
        |6 | Length - equals [length =]   |
        |7 | Length - not equal [length !=]|
        |8 | Length - greater than [length >]   |
        |9 | Length - less than [length <]   |
        |10    | Value - contains [ include =]   |
        |11    | Value - greater than or equal to [value >=] |
        |12    | Value - less than or equal to [value <=] |
        |13    | Value - does not contain [ include !=]|
  - child_list: List of sub-parameter verification rules

## Rules for constructing array type parameters:
Please first distinguish whether this array type parameter is encountered when constructing params request parameters or when constructing parameter matching rules for response body verification!
### When you need to construct array type parameters in params request parameters
**This rule only applies to params request parameters, please do not use it in match_rule of response body verification!!!**
**This rule only applies to params request parameters, please do not use it in match_rule of response body verification!!!**
**This rule only applies to params request parameters, please do not use it in match_rule of response body verification!!!**
1. Array element representation:
- When the parameter is of array type, when constructing the parameter, you need to represent the param_key of each element in the child_list field in the form of item[n], where n is the index of the array.
2. Distinguish between array of objects and ordinary arrays:
- If the array type parameter has sub-parameters, it is an array of objects.
- If the array type parameter does not have sub-parameters, it is an ordinary array.
3. Array of objects construction rules:
- Use item[n] to represent the param_key of an object element in the array, then the param_type corresponding to item[n] is object (13), and each object contains multiple sub-parameters.
- Sub-parameter construction is placed in the child_list field under the item[n] object.
- Multiple parameter sets have multiple item objects.
- Example:
(In this example, personInfo is an array type parameter encountered when constructing params request parameters)
{{
    "param_type": "12",
    "param_key": "personInfo",
    "param_info": "",
    "child_list": [
        {{
            "param_type": "13",
            "param_key": "item[0]",
            "param_info": "",
            "is_arr_item": true,
            "child_list": [
                {{
                    "param_type": "0",
                    "param_key": "name",
                    "param_info": "Zhang San",
                    "child_list": []
                }},
                {{
                    "param_type": "14",
                    "param_key": "age",
                    "param_info": "11",
                    "child_list": []
                }}
            ]
        }},
        {{
            "param_type": "13",
            "param_key": "item[1]",
            "param_info": "",
            "is_arr_item": true,
            "child_list": [
                {{
                    "param_type": "0",
                    "param_key": "name",
                    "param_info": "Li Si",
                    "child_list": []
                }},
                {{
                    "param_type": "14",
                    "param_key": "age",
                    "param_info": "19",
                    "child_list": []
                }}
            ]
        }}
    ]
}}
4. Ordinary array construction rules:
- Use item[n] to represent a basic type element in the array (such as a string or number).
- The parameter value is directly placed in the param_info of the structure with param_key as item[n].
- Example
(In this example, nameList is an array type parameter encountered when constructing params request parameters)
{{
    "param_type": "12",
    "param_key": "nameList",
    "param_info":