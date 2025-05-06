#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Mock data for API documentation, including array format data,
# Reference address http://devapi.sangfor.com/independent/home/api-studio/inside/IvrAAgq34371b47badaf040f4efcd8378d0b0a0fe99a657/
# api/689818/detail/2161015?spaceKey=iDsnTP3074a43c21500a0945db409e159e9c905f55c7fcd
MOCK_API_INFO_ARRAY = {
    "baseInfo": {
        "apiName": "Create Prompt Square Data",
        "apiURI": "/api/prompt_square",
        "apiProtocol": 0,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 0,
        "starred": 0,
        "apiNoteType": 1,
        "apiNoteRaw": "##### Interface Purpose\r\n\r\nUsed to share your prompt to the square for others to view",
        "apiNote": "<h5>Interface Purpose</h5><p>Used to share your prompt to the square for others to view</p>",
        "apiRequestParamType": 2,
        "apiRequestRaw": "",
        "apiRequestBinary": "",
        "apiFailureStatusCode": "403",
        "apiSuccessStatusCode": "200",
        "apiFailureContentType": "application/json",
        "apiSuccessContentType": "application/json",
        "apiRequestParamJsonType": 0,
        "advancedSetting": None,
        "beforeInject": "",
        "afterInject": "",
        "createTime": "2023-03-28 09:21:52",
        "apiUpdateTime": "2024-05-16 10:55:46",
        "apiTag": "",
        "beforeScriptMode": 1,
        "afterScriptMode": 1,
        "beforeScriptList": [],
        "afterScriptList": [],
        "removed": 0,
        "sampleURI": "http://devapi.sangfor.com/index.php/apiManagementPro/Mock/simple",
        "mockCode": "IvrAAgq34371b47badaf040f4efcd8378d0b0a0fe99a657?uri=/api/prompt_square",
        "apiID": 2161015,
        "groupID": 689818,
        "groupPath": "689819,689818",
        "apiRequestMetadata": [],
        "responseMetadata": [],
        "responseTrailingMetadata": [],
        "groupName": "Prompt Square",
        "apiManagerConnID": 25,
        "creator": "Fan Liwei",
        "updater": "Fan Liwei",
        "apiManager": "Engineering Productivity"
    },
    "responseHeader": [],
    "headerInfo": [],
    "authInfo": {
        "status": "0"
    },
    "requestInfo": [
        {
            "paramNotNone": "0",
            "paramType": "0",
            "paramName": " Title",
            "paramKey": "title",
            "paramValue": "a51",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "childList": []
        },
        {
            "paramNotNone": "0",
            "paramType": "3",
            "paramName": " Title",
            "paramKey": "int_data",
            "paramValue": "123",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "childList": []
        },
        {
            "paramNotNone": "0",
            "paramType": "12",
            "paramName": " Q&A Data",
            "paramKey": "prompt_completion",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "childList": [
                {
                    "paramNotNone": "0",
                    "paramType": "0",
                    "paramName": " Question",
                    "paramKey": "prompt",
                    "paramValue": "xx",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": []
                },
                {
                    "paramNotNone": "0",
                    "paramType": "0",
                    "paramName": " Answer",
                    "paramKey": "completion",
                    "paramValue": "xx",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": []
                },
                {
                    "paramNotNone": "0",
                    "paramType": "0",
                    "paramName": " Question Time ",
                    "paramKey": "prompt_time",
                    "paramValue": "2023/3/23 PM 7:35:48",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": []
                },
                {
                    "paramNotNone": "0",
                    "paramType": "0",
                    "paramName": " Answer Time",
                    "paramKey": "completion_time",
                    "paramValue": "2023/3/23 PM 7:35:48",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": []
                }
            ]
        }
    ],
    "urlParam": [],
    "restfulParam": [],
    "resultInfo": [
        {
            "responseID": 13035,
            "responseCode": "200",
            "responseName": "Success",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "paramNotNull": "0",
                    "paramName": "",
                    "paramKey": "data",
                    "paramType": "13",
                    "paramValueList": [],
                    "childList": [
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "created_at",
                            "paramType": "0",
                            "paramValueList": [],
                            "paramValue": "2023-04-20T14:07:16.000+0800",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "creator",
                            "paramType": "0",
                            "paramValueList": [],
                            "paramValue": "test",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "deleted",
                            "paramType": "8",
                            "paramValueList": [],
                            "paramValue": "false",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "hot",
                            "paramType": "14",
                            "paramValueList": [],
                            "paramValue": "0",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "id",
                            "paramType": "14",
                            "paramValueList": [],
                            "paramValue": "22",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "prompt",
                            "paramType": "0",
                            "paramValueList": [],
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0,
                            "paramValue": ""
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "prompt_completion",
                            "paramType": "12",
                            "paramValueList": [],
                            "childList": [
                                {
                                    "paramNotNull": "0",
                                    "paramName": "",
                                    "paramKey": "completion",
                                    "paramType": "0",
                                    "paramValueList": [],
                                    "paramValue": "xx",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "default": 0
                                },
                                {
                                    "paramNotNull": "0",
                                    "paramName": "",
                                    "paramKey": "completion_time",
                                    "paramType": "0",
                                    "paramValueList": [],
                                    "paramValue": "2023/3/23 PM 7:35:48",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "default": 0
                                },
                                {
                                    "paramNotNull": "0",
                                    "paramName": "",
                                    "paramKey": "prompt",
                                    "paramType": "0",
                                    "paramValueList": [],
                                    "paramValue": "xx",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "default": 0
                                },
                                {
                                    "paramNotNull": "0",
                                    "paramName": "",
                                    "paramKey": "prompt_time",
                                    "paramType": "0",
                                    "paramValueList": [],
                                    "paramValue": "2023/3/23 PM 7:35:48",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "default": 0
                                }
                            ],
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0,
                            "paramValue": ""
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "title",
                            "paramType": "0",
                            "paramValueList": [],
                            "paramValue": "a5112",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        },
                        {
                            "paramNotNull": "0",
                            "paramName": "",
                            "paramKey": "update_at",
                            "paramType": "0",
                            "paramValueList": [],
                            "paramValue": "2023-04-20T14:07:16.000+0800",
                            "paramLimit": "",
                            "paramNote": "",
                            "default": 0
                        }
                    ],
                    "paramLimit": "",
                    "paramNote": "",
                    "default": 0,
                    "paramValue": ""
                },
                {
                    "paramNotNull": "0",
                    "paramName": "",
                    "paramKey": "message",
                    "paramType": "0",
                    "paramValueList": [],
                    "paramValue": "Successfully retrieved",
                    "paramLimit": "",
                    "paramNote": "",
                    "default": 0
                },
                {
                    "paramNotNull": "0",
                    "paramName": "",
                    "paramKey": "success",
                    "paramType": "8",
                    "paramValueList": [],
                    "paramValue": "true",
                    "paramLimit": "",
                    "paramNote": "",
                    "default": 0
                }
            ],
            "raw": "",
            "binary": "",
            "isDefault": 1
        }
    ],
    "resultParamJsonType": 0,
    "resultParamType": 0,
    "fileID": "",
    "requestParamSetting": {},
    "resultParamSetting": {},
    "customInfo": {
        "messageEncoding": "utf-8"
    },
    "soapVersion": None,
    "version": 1040,
    "tagID": [],
    "wsdlContent": "",
    "testData": "",
    "defaultResponseID": 13035,
    "mockList": [],
    "apiType": "http",
    "dbFieldObj": {},
    "apiID": "2161015",
    "customizeList": [],
    "manager": "Engineering Productivity",
    "creator": "Fan Liwei",
    "updater": "Fan Liwei",
    "noticeType": 0,
    "fileList": [],
    "dataStructureList": []
}

MOCK_TEST_STEPS_ARRAY_ERROR = [
    {
        "api_id": 2161015,
        "api_name": "Prerequisite Step-Create Prompt Square Data",
        "api_url": "/api/prompt_square",
        "api_protocol": 0,
        "case_data": {
            "url": "/api/prompt_square",
            "step_type": "api_request",
            "api_request_type": "0",
            "headers": [],
            "url_param": [],
            "restful_param": [],
            "params": [
                {
                    "param_type": "13",
                    "param_key": "title",
                    "param_info": "Test Title",
                    "child_list": []
                },
                {
                    "param_type": "13",
                    "param_key": "int_data",
                    "param_info": "123",
                    "child_list": []
                },
                {
                    "param_type": "13",
                    "param_key": "prompt_completion",
                    "param_info": "Test Question",
                    "child_list": [
                        {
                            "param_type": "0",
                            "param_key": "prompt",
                            "param_info": "Test Question",
                            "child_list": []
                        }
                    ]
                }
            ],
            "requestType": "2"
        },
        "status_code_verification": {
            "check_status": True,
            "status_code": 200
        },
        "response_result_verification": {
            "check_status": True,
            "param_match": "json",
            "json_result_verification": {
                "result_type": "object",
                "match_rule": "allElement"
            },
            "match_rule": []
        }
    }
]

MOCK_TEST_STEPS_ARRAY_CORRECT = [
    {
        "api_id": 2161015,
        "api_name": "Prerequisite Step-Create Prompt Square Data",
        "api_url": "/api/prompt_square",
        "api_protocol": 0,
        "case_data": {
            "url": "/api/prompt_square",
            "step_type": "api_request",
            "api_request_type": "0",
            "headers": [],
            "url_param": [],
            "restful_param": [],
            "params": [
                {
                    "param_type": "0",
                    "param_key": "title",
                    "param_info": "Test Title",
                    "child_list": []
                },
                {
                    "param_type": "14",
                    "param_key": "int_data",
                    "param_info": "123",
                    "child_list": []
                },
                {
                    "param_type": "12",
                    "param_key": "prompt_completion",
                    "param_info": "Test Question",
                    "child_list": [
                        {
                            "param_type": "13",
                            "param_key": "item[0]",
                            "param_info": "",
                            "is_arr_item": True,
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "prompt",
                                    "param_info": "Test Question",
                                    "child_list": []
                                }
                            ]
                        }
                    ]
                }
            ],
            "requestType": "2"
        },
        "status_code_verification": {
            "check_status": True,
            "status_code": 200
        },
        "response_result_verification": {
            "check_status": True,
            "param_match": "json",
            "json_result_verification": {
                "result_type": "object",
                "match_rule": "allElement"
            },
            "match_rule": []
        }
    }
]

MOCK_TEST_STEPS_PARAM_KEY_ERROR = [
    {
        "api_id": 2161011,
        "api_name": "Main Test Step-Request GPT Interface and Set systems Parameters",
        "api_url": "/api/v2/completion",
        "api_protocol": 0,
        "case_data": {
            "url": "/api/v2/completion",
            "step_type": "api_request",
            "api_request_type": "0",
            "headers": [
                {
                    "header_name": "Content-Type",
                    "header_value": "application/json"
                },
                {
                    "header_name": "api-key",
                    "header_value": "your_api_key_here"
                }
            ],
            "url_param": [],
            "restful_param": [],
            "params": [
                {
                    "param_type": "12",
                    "param_key": "systems",
                    "param_info": "",
                    "child_list": [
                        {
                            "param_type": "0",
                            "param_key": "item[0]",
                            "param_info": "system_preset_1",
                            "is_arr_item": True,
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "item[1]",
                            "param_info": "system_preset_2",
                            "is_arr_item": True,
                            "child_list": []
                        }
                    ]
                },
                {
                    "param_type": "0",
                    "param_key": "action",
                    "param_info": "chat",
                    "child_list": []
                }
            ],
            "requestType": "2"
        },
        "status_code_verification": {
            "check_status": True,
            "status_code": 200
        },
        "response_result_verification": {
            "check_status": True,
            "param_match": "json",
            "json_result_verification": {
                "result_type": "object",
                "match_rule": "allElement"
            },
            "match_rule": [
                {
                    "param_key": "choices",
                    "param_info": "",
                    "match_rule": "0",
                    "child_list": [
                        {
                            "check_exist": "1",
                            "param_key": "message.content",
                            "param_info": "0",
                            "match_rule": "8",
                            "child_list": []
                        }
                    ]
                },
                {
                    "check_exist": "1",
                    "param_key": "id",
                    "param_info": "",
                    "match_rule": "8",
                    "child_list": []
                }
            ]
        }
    }
]

MOCK_TEST_STEPS_PARAM_KEY_CORRECT = [
    {
        "api_id": 2161011,
        "api_name": "Main Test Step-Request GPT Interface and Set systems Parameters",
        "api_url": "/api/v2/completion",
        "api_protocol": 0,
        "case_data": {
            "url": "/api/v2/completion",
            "step_type": "api_request",
            "api_request_type": "0",
            "headers": [
                {
                    "header_name": "Content-Type",
                    "header_value": "application/json"
                },
                {
                    "header_name": "api-key",
                    "header_value": "your_api_key_here"
                }
            ],
            "url_param": [],
            "restful_param": [],
            "params": [
                {
                    "param_type": "12",
                    "param_key": "systems",
                    "param_info": "",
                    "child_list": [
                        {
                            "param_type": "0",
                            "param_key": "item[0]",
                            "param_info": "system_preset_1",
                            "is_arr_item": True,
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "item[1]",
                            "param_info": "system_preset_2",
                            "is_arr_item": True,
                            "child_list": []
                        }
                    ]
                },
                {
                    "param_type": "0",
                    "param_key": "action",
                    "param_info": "chat",
                    "child_list": []
                }
            ],
            "requestType": "2"
        },
        "status_code_verification": {
            "check_status": True,
            "status_code": 200
        },
        "response_result_verification": {
            "check_status": True,
            "param_match": "json",
            "json_result_verification": {
                "result_type": "object",
                "match_rule": "allElement"
            },
            "match_rule": [
                {
                    "param_key": "choices",
                    "param_info": "",
                    "match_rule": "0",
                    "child_list": [
                        {
                            "check_exist": "1",
                            "param_key": "message",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "check_exist": "1",
                                    "param_key": "content",
                                    "param_info": "0",
                                    "match_rule": "8",
                                    "child_list": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "check_exist": "1",
                    "param_key": "id",
                    "param_info": "0",
                    "match_rule": "8",
                    "child_list": []
                }
            ]
        }
    }
]

MOCK_API_INFO_ARRAY_OBJECT = {
    "baseInfo": {
        "apiName": "Id Association Application",
        "apiURI": "/api/v3/user/assignResourceById",
        "apiProtocol": 1,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 0,
        "starred": 0,
        "apiNoteType": 1,
        "apiRequestParamType": 2,
        "apiRequestRaw": "",
        "apiRequestBinary": "",
        "apiFailureStatusCode": "200",
        "apiSuccessStatusCode": "200",
        "apiFailureContentType": "text/html; charset=UTF-8",
        "apiSuccessContentType": "text/html; charset=UTF-8",
        "apiRequestParamJsonType": 0,
        "beforeInject": "",
        "afterInject": "",
        "createTime": "2024-01-17 14:57:02",
        "apiUpdateTime": "2024-05-31 16:13:50",
        "apiTag": "",
        "beforeScriptMode": 1,
        "afterScriptMode": 1,
        "beforeScriptList": [],
        "afterScriptList": [],
        "removed": 0,
        "sampleURI": "http://devapi.sangfor.com/index.php/apiManagementPro/Mock/simple",
        "mockCode": "IvrAAgq34371b47badaf040f4efcd8378d0b0a0fe99a657?uri=/api/v3/user/assignResourceById",
        "apiID": 2161250,
        "groupID": 689828,
        "groupPath": "689267,689828",
        "apiRequestMetadata": [],
        "responseMetadata": [],
        "responseTrailingMetadata": [],
        "groupName": "ID Association Application",
        "apiManagerConnID": 0,
        "creator": "Fan Liwei",
        "updater": "Su Deli",
    },
    "responseHeader": [],
    "authInfo": {
        "status": "0"
    },
    "requestInfo": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "User ID",
            "paramKey": "id",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "Only one of id and name needs to be passed, when both are passed, id takes precedence",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "The unique identifier of the user directory to which it belongs, the unique identifier of the local user directory is local. External user directory example: custom01339 (the unique identifier does not need to carry @)",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "directoryDomain",
            "paramValue": "ff52b0e2-e101-11ee-8ada-fefcfeefe529"
        },
        {
            "structureID": "69736",
            "updateData": {
                "ABuN6cF9e91b9d76c2611ee088c6188944c2929cec03dc2": {
                    "paramName": "This parameter is required when the resource parameter is filled"
                }
            },
            "childList": []
        }
    ],
    "urlParam": [],
    "restfulParam": [],
    "resultInfo": [
        {
            "responseID": 13054,
            "responseCode": "200",
            "responseName": "Success",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "structureID": "68244",
                    "updateData": {
                        "y9zkLGPbd6658f73861fe3274ce825d422e4fbdc93c5be2": {
                            "paramValue": "OK"
                        },
                        "YfsfgJv09dbc5faf7f28ed7164d35bc67eeaa1eb2c158d0": {
                            "paramNotNull": "1",
                            "paramName": ""
                        }
                    },
                    "childList": []
                }
            ],
            "raw": "",
            "binary": "",
            "isDefault": 1
        },
        {
            "responseID": 13055,
            "responseCode": "200",
            "responseName": "Failed",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "structureID": "68244",
                    "updateData": {
                        "y9zkLGPbd6658f73861fe3274ce825d422e4fbdc93c5be2": {
                            "paramName": "Error code information",
                            "paramValue": "NotExist.Resource"
                        },
                        "YfsfgJv09dbc5faf7f28ed7164d35bc67eeaa1eb2c158d0": {
                            "paramName": ""
                        }
                    },
                    "childList": []
                }
            ],
            "raw": "",
            "binary": "",
            "isDefault": 0
        }
    ],
    "resultParamJsonType": 0,
    "resultParamType": 0,
    "fileID": "",
    "requestParamSetting": {},
    "resultParamSetting": {},
    "customInfo": {
        "messageEncoding": "utf-8"
    },
    "version": 1040,
    "tagID": [],
    "wsdlContent": "",
    "testData": "",
    "defaultResponseID": 13054,
    "mockList": [],
    "apiManagerID": 0,
    "apiType": "http",
    "dbFieldObj": {},
    "apiID": "2161250",
    "customizeList": [],
    "creator": "Fan Liwei",
    "updater": "Su Deli",
    "noticeType": 0,
    "fileList": [],
    "dataStructureList": {
        "68244": {
            "structureID": 68244,
            "structureName": "SDP-TEST-POST Common Return Data",
            "structureDesc": "",
            "updateTime": "2024-05-21 14:23:26",
            "structureData": [
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "OK means success, others mean error. Please refer to error code definition for specific meaning",
                    "paramKey": "code",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "y9zkLGPbd6658f73861fe3274ce825d422e4fbdc93c5be2"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "Message data body",
                    "paramKey": "data",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "WrXKbXI33c9c426d87dea74bd7c7ff34a12c71b4b837e7d"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "Return prompt information, corresponding to the return code",
                    "paramKey": "msg",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "YfsfgJv09dbc5faf7f28ed7164d35bc67eeaa1eb2c158d0"
                }
            ],
            "structureType": "15",
            "removed": 0,
            "paramStructIdList": []
        },
        "69736": {
            "structureID": 69736,
            "structureName": "resource",
            "structureDesc": "",
            "updateTime": "2024-05-30 14:39:21",
            "structureData": [
                {
                    "paramNotNull": "1",
                    "paramType": "13",
                    "paramName": "应用列表",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "resource",
                    "paramValue": "",
                    "childList": [
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "操作类型。 取值范围： append-追加更新（默认） reset-重置 delete-删除",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [
                                {
                                    "paramType": "0",
                                    "radio": True,
                                    "value": "append",
                                    "valueDescription": "追加更新（默认）"
                                },
                                {
                                    "paramType": "0",
                                    "radio": False,
                                    "value": "reset",
                                    "valueDescription": "重置"
                                },
                                {
                                    "paramType": "0",
                                    "radio": False,
                                    "value": "delete",
                                    "valueDescription": "删除"
                                }
                            ],
                            "default": 0,
                            "paramKey": "op",
                            "paramValue": "",
                            "paramID": "13ButaBb564e10481a838775eac3265153ffc4a822563e5",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "key 是指标识应用的对象，即通过什么方式（或值）来授权指定的应用。零信任提供了两种标识来定义应用，即 id/name。 存在 resource 参数时，此参数必传。 取值范围： id-应用id name-应用名称",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [
                                {
                                    "paramType": "0",
                                    "radio": True,
                                    "value": "id",
                                    "valueDescription": "应用id"
                                },
                                {
                                    "paramType": "0",
                                    "radio": False,
                                    "value": "name",
                                    "valueDescription": "应用名称"
                                }
                            ],
                            "default": 0,
                            "paramKey": "key",
                            "paramValue": "",
                            "paramID": "bS4KPA93281bdd586d19ea4a67835c8bdd1c9ba83ec7396",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "12",
                            "paramName": "存在 resource 参数时，此参数必传。",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "data",
                            "paramValue": "",
                            "childList": [
                                {
                                    "paramNotNull": "1",
                                    "paramType": "0",
                                    "paramName": "data 是 key 值的结果，即若 key 的赋值是 name，那么 data 对应的赋值就是应用名，如: \"mail\"。若 key 的赋值是 id，那么 data 就需要写应用的 id 值。 存在 resource 参数时，此参数必传。 key 与 data 的对应取值示例如下： id：1345c177-e4f6-11ee-835b-fefcfeefe529 name：mail",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "paramValueList": [],
                                    "default": 0,
                                    "paramKey": "data",
                                    "paramValue": "",
                                    "paramID": "lSLTmpk43cd64f3abe07284ed11000848dbc12c466ab445",
                                    "childList": []
                                },
                                {
                                    "paramNotNull": "1",
                                    "paramType": "0",
                                    "paramName": "授权生效时间,支持毫秒级别的Unix时间戳，以及时间字符串格式如：2024-03-18 12:00:00。 不传时默认立刻生效。 示例： 时间戳：1710745688563 时间字符串：2024-03-18 12:00:00、2024/03/18 12:00:00",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "paramValueList": [],
                                    "default": 0,
                                    "paramKey": "effectiveTime",
                                    "paramValue": "",
                                    "paramID": "plhnB92be732d46027ab7825f9decf0fab815df1312689f",
                                    "childList": []
                                },
                                {
                                    "paramNotNull": "1",
                                    "paramType": "0",
                                    "paramName": "授权过期时间，支持毫秒级别的Unix时间戳，以及时间字符串格式如：2024-03-18 12:00:00。 不传时默认永不过期。 示例： 时间戳：1710745688563 时间字符串：2024-03-18 12:00:00、2024/03/18 12:00:00",
                                    "paramLimit": "",
                                    "paramNote": "",
                                    "paramValueList": [],
                                    "default": 0,
                                    "paramKey": "expireTime",
                                    "paramValue": "",
                                    "paramID": "C5ek3ad0c325e1569edc43aff2a24a4e20b515b97f12642",
                                    "childList": []
                                }
                            ],
                            "paramID": "ABuN6cF9e91b9d76c2611ee088c6188944c2929cec03dc2"
                        }
                    ],
                    "paramID": "kaJRXCS5cb6ec9aac0861be90ad9ab26630af1899230c10"
                }
            ],
            "structureType": "13",
            "removed": 0,
            "paramStructIdList": []
        }
    }
}

MOCK_TEST_STEPS_ARRAY_OBJECT_ERROR = [
    {
        "api_id": 2161250,
        "api_name": "主步骤-为用户授权单个应用",
        "api_url": "/api/v3/user/assignResourceById",
        "api_protocol": 1,
        "case_data": {
            "url": "/api/v3/user/assignResourceById",
            "step_type": "api_request",
            "api_request_type": "0",
            "headers": [
                {
                    "header_name": "Content-Type",
                    "header_value": "application/json"
                }
            ],
            "url_param": [],
            "restful_param": [],
            "params": [
                {
                    "param_type": "0",
                    "param_key": "id",
                    "param_info": "step[1]['response']['data']['id']",
                    "child_list": []
                },
                {
                    "param_type": "0",
                    "param_key": "directoryDomain",
                    "param_info": "local",
                    "child_list": []
                },
                {
                    "param_type": "13",
                    "param_key": "resource",
                    "param_info": "",
                    "child_list": [
                        {
                            "param_type": "0",
                            "param_key": "op",
                            "param_info": "append",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "key",
                            "param_info": "id",
                            "child_list": []
                        },
                        {
                            "param_type": "12",
                            "param_key": "data",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "item[0]",
                                    "param_info": "step[2]['response']['data']['data'][0]['id']",
                                    "is_arr_item": True
                                }
                            ]
                        }
                    ]
                }
            ],
            "requestType": "2"
        },
        "status_code_verification": {
            "check_status": True,
            "status_code": 200
        },
        "response_result_verification": {
            "check_status": True,
            "param_match": "json",
            "json_result_verification": {
                "result_type": "object",
                "match_rule": "allElement"
            },
            "match_rule": [
                {
                    "param_key": "code",
                    "param_info": "OK",
                    "match_rule": "1",
                    "child_list": []
                }
            ]
        }
    }
]
