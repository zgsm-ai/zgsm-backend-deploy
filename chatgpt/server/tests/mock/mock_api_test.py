#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Mock data for API documentation
MOCK_API_INFO1 = {
    "baseInfo": {
        "apiName": "Modify User",
        "apiURI": "/api/v1/users/{id}",
        "apiProtocol": 0,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 0,
        "starred": 0,
        "apiNoteType": 1,
        "apiNoteRaw": "User modification interface\r\n**A good interface**",
        "apiNote": "<p>User modification interface</p><p><strong>A good interface</strong></p>",
        "apiRequestParamType": 2,
        "apiRequestRaw": "",
        "apiRequestBinary": "",
        "apiFailureStatusCode": "200",
        "apiSuccessStatusCode": "200",
        "apiFailureContentType": "text/html; charset=UTF-8",
        "apiSuccessContentType": "text/html; charset=UTF-8",
        "apiRequestParamJsonType": 0,
        "advancedSetting": None,
        "beforeInject": "",
        "afterInject": "",
        "createTime": "2021-04-09 17:38:41",
        "apiUpdateTime": "2024-03-18 20:00:30",
        "apiTag": "",
        "beforeScriptMode": 1,
        "afterScriptMode": 1,
        "beforeScriptList": [],
        "afterScriptList": [],
        "removed": 0,
        "sampleURI": "http://devapi.sangfor.com/index.php/apiManagementPro/Mock/simple",
        "mockCode": "sfKq7HD42045a821b8f5490dfaa0e30b86d1b79c0bf1347?uri=/api/v1/users/{id}",
        "apiID": 16344,
        "groupID": 1822,
        "groupPath": "1822",
        "apiRequestMetadata": [],
        "responseMetadata": [],
        "responseTrailingMetadata": [],
        "groupName": "Users",
        "apiManagerConnID": 0,
        "creator": "Fan Liwei",
        "updater": "Fan Liwei",
        "apiManager": None
    },
    "responseHeader": [],
    "headerInfo": [],
    "authInfo": {
        "status": "0"
    },
    "requestInfo": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "(Required) User phone number",
            "paramKey": "mobile",
            "paramValue": "12345678987",
            "paramLimit": "11-digit China mainland phone number",
            "paramNote": "Phone",
            "paramValueList": [],
            "childList": [],
            "default": "",
            "minLength": 11,
            "maxLength": 11
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "(Required) User password",
            "paramKey": "password",
            "paramValue": "111111",
            "paramLimit": "Numbers, letters",
            "paramNote": "Password",
            "paramValueList": [],
            "childList": [],
            "default": "",
            "minLength": 6,
            "maxLength": 6
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "(Required) User SMS verification code",
            "paramKey": "sms_code",
            "paramValue": "213",
            "paramLimit": "Numeric only",
            "paramNote": "sms",
            "paramValueList": [],
            "childList": [],
            "default": "",
            "minLength": 3,
            "maxLength": 3
        },
        {
            "paramNotNull": "0",
            "paramType": "13",
            "paramName": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "address",
            "paramValue": "",
            "childList": [
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "Address name",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "name",
                    "paramValue": ""
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "Email",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "mail",
                    "paramValue": ""
                }
            ]
        }
    ],
    "urlParam": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "aaa",
            "paramValue": ""
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "vvv",
            "paramValue": ""
        }
    ],
    "restfulParam": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "id",
            "paramValue": ""
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "cccc",
            "paramValue": ""
        }
    ],
    "resultInfo": [
        {
            "responseID": 871,
            "responseCode": "200",
            "responseName": "Success",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "paramNotNull": "0",
                    "paramType": "3",
                    "paramName": "User registration id",
                    "paramKey": "user_id",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": ""
                }
            ]
        }
    ]
}

# Continue with the rest of the file...
# The file is very large, but I'll only translate the Chinese parts
