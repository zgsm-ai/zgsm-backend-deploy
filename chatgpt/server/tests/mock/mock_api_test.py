#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2024/3/18 19:58
"""

# api文档的模拟数据
MOCK_API_INFO1 = {
    "baseInfo": {
        "apiName": "修改用户",
        "apiURI": "/api/v1/users/{id}",
        "apiProtocol": 0,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 0,
        "starred": 0,
        "apiNoteType": 1,
        "apiNoteRaw": "修改用户接口\r\n**一个好的接口**",
        "apiNote": "<p>修改用户接口</p><p><strong>一个好的接口</strong></p>",
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
        "creator": "范立伟",
        "updater": "范立伟",
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
            "paramName": "(必须)    用户手机号",
            "paramKey": "mobile",
            "paramValue": "12345678987",
            "paramLimit": "11位中国大陆手机号",
            "paramNote": "手机",
            "paramValueList": [],
            "childList": [],
            "default": "",
            "minLength": 11,
            "maxLength": 11
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "(必须)    用户密码",
            "paramKey": "password",
            "paramValue": "111111",
            "paramLimit": "数字、英文",
            "paramNote": "密码",
            "paramValueList": [],
            "childList": [],
            "default": "",
            "minLength": 6,
            "maxLength": 6
        },
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "(必须)    用户短信验证码",
            "paramKey": "sms_code",
            "paramValue": "213",
            "paramLimit": "纯数字",
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
                    "paramName": "地址名称",
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
                    "paramName": "邮箱",
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
            "responseName": "成功",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "paramNotNull": "0",
                    "paramType": "3",
                    "paramName": "用户注册id",
                    "paramKey": "user_id",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": ""
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "用户昵称",
                    "paramKey": "name",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": ""
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "用户注册手机号",
                    "paramKey": "mobile",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": ""
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "用户头像地址",
                    "paramKey": "avatar",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": ""
                },
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "用户创建时间",
                    "paramKey": "create_time",
                    "paramValue": None,
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": "",
                    "childList": [
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "123",
                            "paramValue": ""
                        }
                    ]
                },
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "aaa",
                    "paramValue": ""
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
    "wsdlContent": "",
    "testData": "",
    "defaultResponseID": 871,
    "mockList": [
        {
            "name": "系统默认期望",
            "source": "高级Mock",
            "url": "/sfKq7HD42045a821b8f5490dfaa0e30b86d1b79c0bf1347/api/v1/users/{id}",
            "mockServer": "https://devapi.sangfor.com/httpMock/mockApi"
        },
        {
            "name": "成功(200)",
            "source": "接口返回",
            "url": "/sfKq7HD42045a821b8f5490dfaa0e30b86d1b79c0bf1347/api/v1/users/{id}?responseId=871",
            "mockServer": "https://devapi.sangfor.com/httpMock/mockApi"
        }
    ],
    "apiManagerID": 0,
    "apiType": "http",
    "dbFieldObj": {},
    "tagID": [],
    "apiID": "16344",
    "customizeList": [],
    "creator": "范立伟",
    "updater": "范立伟",
    "noticeType": 0,
    "fileList": [],
    "dataStructureList": []
}

MOCK_API_INFO2 = {
    "baseInfo": {
        "apiName": "副本 - Id更新用户",
        "apiURI": "/api/v3/user/updateById/new",
        "apiProtocol": 1,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 8,
        "starred": 0,
        "apiNoteType": 1,
        "apiNoteRaw": "**接口描述：**\r\n\r\n1. 对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改\r\n2. 参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。\r\n3. 对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改\r\n4. 认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”->“认证管理”->“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID\r\n5. 用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”->“策略管理”->“用户策略”页面，查看响应体数据获取所需策略的ID\r\n\r\n**请求示例**\r\n\r\n```json\r\n{\r\n\t\"id\": \"23c916f0-5583-11eb-880a-913383f106f2\",\r\n\t\"status\": 1,\r\n\t\"description\": \"sdsa\",\r\n\t\"email\": \"\",\r\n\t\"phone\": \"\",\r\n\t\"groupId\": \"1059f620-5583-11eb-880a-913383f106f2\",\r\n\t\"expiredTime\": \"0\",\r\n\t\"inheritGroup\": 1,\r\n\t\"roleIdList\": [\"3359f620-5583-11eb-880a-913383f106f2\"],\r\n\t\"roleIdEditWay\": \"append\",\r\n    \"authComposeId\": \"fbda378b-fa23-4e8b-b4a7-cf7f979cd85b\",\r\n    \"userPolicyId\": \"88040d85-0e58-432c-8568-4c5a8e1907ef\"\r\n}\r\n```\r\n\r\n**错误信息**\r\n\r\n| 错误提示 | 错误码 |\r\n| ---- | --- |\r\n| 参数检查失败 | 10000001 |\r\n| 用户最多关联1000个应用 | 10000000 |\r\n| 密码不能属于常见弱密码 | 10000001 |\r\n| 管理员无该操作权限 | 10000000 |\r\n| 用户不存在 | 77200004 |\r\n| 外部ID重复，请重新输入 | 10000000 |\r\n| 密码不能包含用户名 | 10000000 |\r\n| 用户名不允许被编辑 | 10000000 |\r\n| 用户组织架构不存在 | 10000001 |\r\n| 认证策略不存在 | 77200004 |\r\n| 用户策略不存在 | 77200004 |\r\n| 数据已经变动, 请刷新后重试 | 10000001 |\r\n| 保存失败，关联的应用不存在或已被删除 | 77200004 |\r\n| 保存失败，关联的应用分类不存在或已被删除 | 77200004 |\r\n| 用户最多关联1000个应用 | 77200004 |\r\n| 普通管理员不允许修改超级管理员 | 10000001 |\r\n| 超级管理员角色不允许被编辑 | 10000001 |\r\n| 超级管理员状态不允许被编辑 | 10000001 |\r\n| 超级管理员过期时间不允许被编辑 | 10000001 |\r\n| 密码不能包含用户名 | 10000000 |\r\n| 管理员原密码不匹配 | 10000000 |\r\n| 新旧密码不能相同 | 10000000 |\r\n| 认证策略中开启了短信认证，但超级管理员没有手机号码 | 77200021 |\r\n| 超级管理员角色不允许被分配 | 10000001 |\r\n| 管理员角色不存在 | 77200005 |\r\n| 操作失败 | 10000000 |",
        "apiNote": "<p><strong>接口描述：</strong></p><ol><li><p>对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改</p></li><li><p>参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。</p></li><li><p>对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改</p></li><li><p>认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”-&gt;“认证管理”-&gt;“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID</p></li><li><p>用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”-&gt;“策略管理”-&gt;“用户策略”页面，查看响应体数据获取所需策略的ID</p></li></ol><p><strong>请求示例</strong></p><div data-language=\"json\" class=\"toastui-editor-ww-code-block-highlighting\"><pre class=\"language-json\"><code data-language=\"json\" class=\"language-json\"><span class=\"token punctuation\">{</span>\r\n\t<span class=\"token property\">\"id\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"23c916f0-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"status\"</span><span class=\"token operator\">:</span> <span class=\"token number\">1</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"description\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"sdsa\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"email\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"phone\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"groupId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"1059f620-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"expiredTime\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"0\"</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"inheritGroup\"</span><span class=\"token operator\">:</span> <span class=\"token number\">1</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"roleIdList\"</span><span class=\"token operator\">:</span> <span class=\"token punctuation\">[</span><span class=\"token string\">\"3359f620-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">]</span><span class=\"token punctuation\">,</span>\r\n\t<span class=\"token property\">\"roleIdEditWay\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"append\"</span><span class=\"token punctuation\">,</span>\r\n    <span class=\"token property\">\"authComposeId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"fbda378b-fa23-4e8b-b4a7-cf7f979cd85b\"</span><span class=\"token punctuation\">,</span>\r\n    <span class=\"token property\">\"userPolicyId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"88040d85-0e58-432c-8568-4c5a8e1907ef\"</span>\r\n<span class=\"token punctuation\">}</span></code></pre></div><p><strong>错误信息</strong></p><table><thead><tr><th><p>错误提示</p></th><th><p>错误码</p></th></tr></thead><tbody><tr><td><p>参数检查失败</p></td><td><p>10000001</p></td></tr><tr><td><p>用户最多关联1000个应用</p></td><td><p>10000000</p></td></tr><tr><td><p>密码不能属于常见弱密码</p></td><td><p>10000001</p></td></tr><tr><td><p>管理员无该操作权限</p></td><td><p>10000000</p></td></tr><tr><td><p>用户不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>外部ID重复，请重新输入</p></td><td><p>10000000</p></td></tr><tr><td><p>密码不能包含用户名</p></td><td><p>10000000</p></td></tr><tr><td><p>用户名不允许被编辑</p></td><td><p>10000000</p></td></tr><tr><td><p>用户组织架构不存在</p></td><td><p>10000001</p></td></tr><tr><td><p>认证策略不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>用户策略不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>数据已经变动, 请刷新后重试</p></td><td><p>10000001</p></td></tr><tr><td><p>保存失败，关联的应用不存在或已被删除</p></td><td><p>77200004</p></td></tr><tr><td><p>保存失败，关联的应用分类不存在或已被删除</p></td><td><p>77200004</p></td></tr><tr><td><p>用户最多关联1000个应用</p></td><td><p>77200004</p></td></tr><tr><td><p>普通管理员不允许修改超级管理员</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员角色不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员状态不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员过期时间不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>密码不能包含用户名</p></td><td><p>10000000</p></td></tr><tr><td><p>管理员原密码不匹配</p></td><td><p>10000000</p></td></tr><tr><td><p>新旧密码不能相同</p></td><td><p>10000000</p></td></tr><tr><td><p>认证策略中开启了短信认证，但超级管理员没有手机号码</p></td><td><p>77200021</p></td></tr><tr><td><p>超级管理员角色不允许被分配</p></td><td><p>10000001</p></td></tr><tr><td><p>管理员角色不存在</p></td><td><p>77200005</p></td></tr><tr><td><p>操作失败</p></td><td><p>10000000</p></td></tr></tbody></table>",
        "apiRequestParamType": 2,
        "apiRequestRaw": "",
        "apiRequestBinary": "",
        "apiFailureStatusCode": "200",
        "apiSuccessStatusCode": "200",
        "apiFailureContentType": "text/html; charset=UTF-8",
        "apiSuccessContentType": "text/html; charset=UTF-8",
        "apiRequestParamJsonType": 1,
        "advancedSetting": None,
        "beforeInject": "",
        "afterInject": "",
        "createTime": "2024-03-19 17:51:05",
        "apiUpdateTime": "2024-03-19 19:38:13",
        "apiTag": "",
        "beforeScriptMode": 1,
        "afterScriptMode": 1,
        "beforeScriptList": [],
        "afterScriptList": [],
        "removed": 0,
        "sampleURI": "http://10.65.155.46:8077/index.php/apiManagementPro/Mock/simple",
        "mockCode": "testsdp?uri=/api/v3/user/updateById/new",
        "apiID": 246,
        "groupID": 61,
        "groupPath": "61",
        "apiRequestMetadata": [],
        "responseMetadata": [],
        "responseTrailingMetadata": [],
        "groupName": "ID更新用户",
        "apiManagerConnID": 0,
        "creator": "李文静",
        "updater": "李文静",
        "apiManager": None
    },
    "responseHeader": [],
    "headerInfo": [
        {
            "headerName": "Content-Type",
            "headerValue": "application/json",
            "paramNotNull": "0",
            "default": 0,
            "paramType": "0"
        }
    ],
    "authInfo": {
        "status": "0"
    },
    "requestInfo": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "用户ID",
            "paramKey": "id",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "id与name只传一个即可，都传时以id为准",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "用户名",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "name",
            "paramValue": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "外部ID",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "externalId",
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
            "paramKey": "directoryDomain",
            "paramValue": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "13",
            "paramName": "所属组",
            "paramKey": "group",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "可用组织架构的查询接口获取",
            "paramValueList": [],
            "default": "",
            "childList": [
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "op",
                    "paramValue": "set"
                },
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "key",
                    "paramValue": "id"
                },
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "data",
                    "paramValue": "/"
                },
                {
                    "structureID": "1221",
                    "updateData": [],
                    "childList": []
                }
            ]
        },
        {
            "paramNotNull": "1",
            "paramType": "14",
            "paramName": "启用状态：0禁用，1启用",
            "paramKey": "status",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "描述",
            "paramKey": "description",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "密码加密算法类型：'clear'明文，'rsa'非对称加密",
            "paramKey": "pwdModel",
            "paramValue": "clear",
            "paramLimit": "",
            "paramNote": "强烈建议使用'rsa'",
            "paramValueList": [
                {
                    "value": "clear",
                    "valueDescription": "",
                    "paramType": "0"
                }
            ],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "密码",
            "paramKey": "password",
            "paramValue": "♂♀☺♪♫◙♂1",
            "paramLimit": "",
            "paramNote": "如果不修改密码则使用默认值，需要修改密码则使用新密码；如果pwdModel使用'rsa'密码模式，需要对密码进行加密",
            "paramValueList": [
                {
                    "value": "♂♀☺♪♫◙♂1",
                    "valueDescription": "",
                    "paramType": "0"
                }
            ],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "手机号码",
            "paramKey": "phone",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "电子邮件",
            "paramKey": "email",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "过期时间，13位长度的Unix时间戳，'0'表示永不过期",
            "paramKey": "expiredTime",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "14",
            "paramName": "继承所属组的应用授权：0不继承，1继承",
            "paramKey": "inheritGroup",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "structureID": "1222",
            "updateData": [],
            "childList": []
        },
        {
            "structureID": "1217",
            "updateData": [],
            "childList": []
        }
    ],
    "urlParam": [],
    "restfulParam": [],
    "resultInfo": [
        {
            "responseID": 331,
            "responseCode": "200",
            "responseName": "成功",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "1212",
                    "paramValue": ""
                },
                {
                    "structureID": "1224",
                    "updateData": [],
                    "childList": []
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
    "wsdlContent": "",
    "testData": "",
    "defaultResponseID": 331,
    "mockList": [
        {
            "name": "系统默认期望",
            "source": "高级Mock",
            "url": "/testsdp/api/v3/user/updateById/new",
            "mockServer": "http://10.65.155.46:11204/mockApi"
        },
        {
            "name": "成功(200)",
            "source": "接口返回",
            "url": "/testsdp/api/v3/user/updateById/new?responseId=331",
            "mockServer": "http://10.65.155.46:11204/mockApi"
        }
    ],
    "apiManagerID": 0,
    "apiType": "http",
    "dbFieldObj": {},
    "tagID": [],
    "apiID": "246",
    "customizeList": [],
    "creator": "李文静",
    "updater": "李文静",
    "noticeType": 0,
    "fileList": [],
    "dataStructureList": {
        "1217": {
            "structureID": 1217,
            "structureName": "dataSource",
            "structureDesc": "仅外部用户有此参数 数据来源，local、server 从本地配置获取，为 local 从用户目录同步和从认证服务器获取为 server",
            "updateTime": "2024-03-19 11:33:31",
            "structureData": [
                {
                    "paramNotNull": "1",
                    "paramType": "13",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "DataSource",
                    "paramValue": "",
                    "childList": [
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "status",
                            "paramValue": "local",
                            "paramID": "edBAqkNe699b9efb84cc760e4f2d5b66104bdbb217d5ee5",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "displayName",
                            "paramValue": "local",
                            "paramID": "IVJETvJ0f362ec52030e17a2043fc5741331156188a0a00",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "email",
                            "paramValue": "local",
                            "paramID": "ys8QNq6944cab4864af4bee011b330904d4b15ceb417459",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "description",
                            "paramValue": "local",
                            "paramID": "bmBLVLh3e0cd1451ce8f04accec1541cbdb4f700ede30ec",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "phone",
                            "paramValue": "local",
                            "paramID": "qRnpHmTf2e5f136240f9d32b9bbd6a4f65d8d016f86a6bd",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "expiredTime",
                            "paramValue": "local",
                            "paramID": "EfTKcJA195360747c074a9c26a19ded9ca0d5a190bf26f4",
                            "childList": []
                        }
                    ],
                    "paramID": "zQB4mbD534fdd0f190c6f6a80cc5868291953f3753f5239"
                }
            ],
            "structureType": "13",
            "removed": 0,
            "paramStructIdList": [],
            "isParsed": True
        },
        "1221": {
            "structureID": 1221,
            "structureName": "group",
            "structureDesc": "",
            "updateTime": "2024-03-19 11:36:21",
            "structureData": [
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "group",
                    "paramValue": "",
                    "childList": [
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "op",
                            "paramValue": "",
                            "paramID": "6ih6jMJdd218470c1de3dd09e2662836000dcb7ff30eab4"
                        },
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "key",
                            "paramValue": "",
                            "paramID": "npygcaIf7ee3583e12db0a182df6ba2d9c8f8be3dfae144",
                            "childList": []
                        },
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "data",
                            "paramValue": "",
                            "paramID": "jsMFu8u4e59f239544af5bc46b08c832c91ebfebdc5c02f",
                            "childList": []
                        }
                    ],
                    "paramID": "7dFp55U8c89c8796ba0c6d744db19b142f0567d07cf2a34"
                }
            ],
            "structureType": "13",
            "removed": 0,
            "paramStructIdList": []
        },
        "1222": {
            "structureID": 1222,
            "structureName": "POST通用返回数据",
            "structureDesc": None,
            "updateTime": "2024-03-19 11:36:40",
            "structureData": [
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "返回码，0 返回成功",
                    "paramKey": "code",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "CBkgpNq6ae40ed6baa3c6c4a9b1a1130dd7499d7fe602aa"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "报文数据主体",
                    "paramKey": "data",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "PxdiEFq8f93dae47434ee311e8b80854ce502684783036c"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "返回提示信息，与返回码对应",
                    "paramKey": "msg",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "ms23P5D85e0d65722e8cfc217f813a52a3a9c71a1a1d34e"
                }
            ],
            "structureType": "15",
            "removed": 0,
            "paramStructIdList": []
        },
        "1224": {
            "structureID": 1224,
            "structureName": "嵌套1",
            "structureDesc": "123",
            "updateTime": "2024-03-19 18:27:28",
            "structureData": [
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "data",
                    "paramValue": "",
                    "paramID": "R9DVsBif1e1465887c8a36a24be58044ab6a8198ff757a3",
                    "childList": [
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "data",
                            "paramValue": "",
                            "paramID": "XAKLBwRfc9d17b5f3d97747359e5c3d16dbb03ee86cffad",
                            "childList": []
                        },
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "effectiveTime",
                            "paramValue": "",
                            "paramID": "qXlcdL5b9f72da78ef04708036451afc72ed341e57d7c0f",
                            "childList": []
                        },
                        {
                            "paramNotNull": "0",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "expireTime",
                            "paramValue": "",
                            "paramID": "4kciXmu9dded90020f10735ef71eca2d80c5e4fc5de8d0d",
                            "childList": []
                        }
                    ]
                },
                {
                    "paramNotNull": "1",
                    "paramType": "13",
                    "paramName": "ffffffff",
                    "paramLimit": "",
                    "paramNote": "aaaaaaaaa",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "DataSource",
                    "paramValue": "",
                    "childList": [
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "ffsssssssssss",
                            "paramLimit": "",
                            "paramNote": "fffff",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "status",
                            "paramValue": "local",
                            "paramID": "edBAqkNe699b9efb84cc760e4f2d5b66104bdbb217d5ee5",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "ddddddd",
                            "paramLimit": "",
                            "paramNote": "fffffff",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "displayName",
                            "paramValue": "local",
                            "paramID": "IVJETvJ0f362ec52030e17a2043fc5741331156188a0a00",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "vc",
                            "paramLimit": "",
                            "paramNote": "vvvvvvvv",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "email",
                            "paramValue": "local",
                            "paramID": "ys8QNq6944cab4864af4bee011b330904d4b15ceb417459",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "c",
                            "paramLimit": "",
                            "paramNote": "vx",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "description",
                            "paramValue": "local",
                            "paramID": "bmBLVLh3e0cd1451ce8f04accec1541cbdb4f700ede30ec",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "vzxc",
                            "paramLimit": "",
                            "paramNote": "xxvczx",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "phone",
                            "paramValue": "local",
                            "paramID": "qRnpHmTf2e5f136240f9d32b9bbd6a4f65d8d016f86a6bd",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "vzxcv",
                            "paramLimit": "",
                            "paramNote": "xzcvdsf",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "expiredTime",
                            "paramValue": "local",
                            "paramID": "EfTKcJA195360747c074a9c26a19ded9ca0d5a190bf26f4",
                            "childList": []
                        }
                    ],
                    "paramID": "zQB4mbD534fdd0f190c6f6a80cc5868291953f3753f5239"
                }
            ],
            "structureType": "15",
            "removed": 0,
            "paramStructIdList": []
        }
    }
}

MOCK_API_INFO3 = {
    "baseInfo": {
        "apiName": "Id更新用户",
        "apiURI": "/api/v3/user/updateById",
        "apiProtocol": 1,
        "apiSuccessMock": "",
        "apiFailureMock": "",
        "apiRequestType": 0,
        "apiStatus": 8,
        "starred": 0,
        "apiNoteType": 1,
        "apiNoteRaw": "**接口描述：**\n\n1. 对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改\n2. 参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。\n3. 对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改\n4. 认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”->“认证管理”->“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID\n5. 用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”->“策略管理”->“用户策略”页面，查看响应体数据获取所需策略的ID\n\n**请求示例**\n\n```json\n{\n\t\"id\": \"23c916f0-5583-11eb-880a-913383f106f2\",\n\t\"status\": 1,\n\t\"description\": \"sdsa\",\n\t\"email\": \"\",\n\t\"phone\": \"\",\n\t\"groupId\": \"1059f620-5583-11eb-880a-913383f106f2\",\n\t\"expiredTime\": \"0\",\n\t\"inheritGroup\": 1,\n\t\"roleIdList\": [\"3359f620-5583-11eb-880a-913383f106f2\"],\n\t\"roleIdEditWay\": \"append\",\n    \"authComposeId\": \"fbda378b-fa23-4e8b-b4a7-cf7f979cd85b\",\n    \"userPolicyId\": \"88040d85-0e58-432c-8568-4c5a8e1907ef\"\n}\n```\n\n**错误信息**\n\n| 错误提示 | 错误码 |\n| ---- | --- |\n| 参数检查失败 | 10000001 |\n| 用户最多关联1000个应用 | 10000000 |\n| 密码不能属于常见弱密码 | 10000001 |\n| 管理员无该操作权限 | 10000000 |\n| 用户不存在 | 77200004 |\n| 外部ID重复，请重新输入 | 10000000 |\n| 密码不能包含用户名 | 10000000 |\n| 用户名不允许被编辑 | 10000000 |\n| 用户组织架构不存在 | 10000001 |\n| 认证策略不存在 | 77200004 |\n| 用户策略不存在 | 77200004 |\n| 数据已经变动, 请刷新后重试 | 10000001 |\n| 保存失败，关联的应用不存在或已被删除 | 77200004 |\n| 保存失败，关联的应用分类不存在或已被删除 | 77200004 |\n| 用户最多关联1000个应用 | 77200004 |\n| 普通管理员不允许修改超级管理员 | 10000001 |\n| 超级管理员角色不允许被编辑 | 10000001 |\n| 超级管理员状态不允许被编辑 | 10000001 |\n| 超级管理员过期时间不允许被编辑 | 10000001 |\n| 密码不能包含用户名 | 10000000 |\n| 管理员原密码不匹配 | 10000000 |\n| 新旧密码不能相同 | 10000000 |\n| 认证策略中开启了短信认证，但超级管理员没有手机号码 | 77200021 |\n| 超级管理员角色不允许被分配 | 10000001 |\n| 管理员角色不存在 | 77200005 |\n| 操作失败 | 10000000 |",
        "apiNote": "<p><strong>接口描述：</strong></p><ol><li><p>对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改</p></li><li><p>参数password密码，为了在数据传输过程中（数据从浏览器/客户端到服务端的过程）保障密码数据的安全，强烈建议使用RSA算法对密码字段进行加密后的密码（将pwdModel参数设置为'rsa'）。加密方式参考详见demo中public模块的encrypt函数，以及handle_rsa.js。如果您不想对密码字段进行加密（强烈不建议如此），可以在请求中不传pwdModel参数或者将pwdModel参数设置为'clear'。</p></li><li><p>对于更新接口中的非必须参数，如果不传，不会对该条数据相对应参数进行修改</p></li><li><p>认证策略ID，authComposeId获取方式，用“开发者工具”过滤请求 authComposeId/queryAll，在控制台“业务管理”-&gt;“认证管理”-&gt;“认证策略”页面中打开您新增用户所属的用户目录，找到所属用户目录的认证策略查询接口，查看响应体数据获取对应的认证策略ID</p></li><li><p>用户策略ID，userPolicyId获取方式，用“开发者工具”过滤请求 userPolicy/queryUserPolicy，进入控制台“业务管理”-&gt;“策略管理”-&gt;“用户策略”页面，查看响应体数据获取所需策略的ID</p></li></ol><p><strong>请求示例</strong></p><div data-language=\"json\" class=\"toastui-editor-ww-code-block-highlighting\"><pre class=\"language-json\"><code data-language=\"json\" class=\"language-json\"><span class=\"token punctuation\">{</span>\n\t<span class=\"token property\">\"id\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"23c916f0-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"status\"</span><span class=\"token operator\">:</span> <span class=\"token number\">1</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"description\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"sdsa\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"email\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"phone\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"groupId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"1059f620-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"expiredTime\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"0\"</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"inheritGroup\"</span><span class=\"token operator\">:</span> <span class=\"token number\">1</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"roleIdList\"</span><span class=\"token operator\">:</span> <span class=\"token punctuation\">[</span><span class=\"token string\">\"3359f620-5583-11eb-880a-913383f106f2\"</span><span class=\"token punctuation\">]</span><span class=\"token punctuation\">,</span>\n\t<span class=\"token property\">\"roleIdEditWay\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"append\"</span><span class=\"token punctuation\">,</span>\n    <span class=\"token property\">\"authComposeId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"fbda378b-fa23-4e8b-b4a7-cf7f979cd85b\"</span><span class=\"token punctuation\">,</span>\n    <span class=\"token property\">\"userPolicyId\"</span><span class=\"token operator\">:</span> <span class=\"token string\">\"88040d85-0e58-432c-8568-4c5a8e1907ef\"</span>\n<span class=\"token punctuation\">}</span></code></pre></div><p><strong>错误信息</strong></p><table><thead><tr><th><p>错误提示</p></th><th><p>错误码</p></th></tr></thead><tbody><tr><td><p>参数检查失败</p></td><td><p>10000001</p></td></tr><tr><td><p>用户最多关联1000个应用</p></td><td><p>10000000</p></td></tr><tr><td><p>密码不能属于常见弱密码</p></td><td><p>10000001</p></td></tr><tr><td><p>管理员无该操作权限</p></td><td><p>10000000</p></td></tr><tr><td><p>用户不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>外部ID重复，请重新输入</p></td><td><p>10000000</p></td></tr><tr><td><p>密码不能包含用户名</p></td><td><p>10000000</p></td></tr><tr><td><p>用户名不允许被编辑</p></td><td><p>10000000</p></td></tr><tr><td><p>用户组织架构不存在</p></td><td><p>10000001</p></td></tr><tr><td><p>认证策略不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>用户策略不存在</p></td><td><p>77200004</p></td></tr><tr><td><p>数据已经变动, 请刷新后重试</p></td><td><p>10000001</p></td></tr><tr><td><p>保存失败，关联的应用不存在或已被删除</p></td><td><p>77200004</p></td></tr><tr><td><p>保存失败，关联的应用分类不存在或已被删除</p></td><td><p>77200004</p></td></tr><tr><td><p>用户最多关联1000个应用</p></td><td><p>77200004</p></td></tr><tr><td><p>普通管理员不允许修改超级管理员</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员角色不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员状态不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>超级管理员过期时间不允许被编辑</p></td><td><p>10000001</p></td></tr><tr><td><p>密码不能包含用户名</p></td><td><p>10000000</p></td></tr><tr><td><p>管理员原密码不匹配</p></td><td><p>10000000</p></td></tr><tr><td><p>新旧密码不能相同</p></td><td><p>10000000</p></td></tr><tr><td><p>认证策略中开启了短信认证，但超级管理员没有手机号码</p></td><td><p>77200021</p></td></tr><tr><td><p>超级管理员角色不允许被分配</p></td><td><p>10000001</p></td></tr><tr><td><p>管理员角色不存在</p></td><td><p>77200005</p></td></tr><tr><td><p>操作失败</p></td><td><p>10000000</p></td></tr></tbody></table>",
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
        "createTime": "2022-11-10 19:23:17",
        "apiUpdateTime": "2024-03-19 11:32:57",
        "apiTag": "",
        "beforeScriptMode": 1,
        "afterScriptMode": 1,
        "beforeScriptList": [],
        "afterScriptList": [],
        "updateUserID": 4,
        "createUserID": 4,
        "removed": 0,
        "sampleURI": "http://10.65.155.46:8077/index.php/apiManagementPro/Mock/simple",
        "mockCode": "testsdp?uri=/api/v3/user/updateById",
        "apiID": 230,
        "groupID": 61,
        "groupPath": "61",
        "apiRequestMetadata": [],
        "responseMetadata": [],
        "responseTrailingMetadata": [],
        "groupName": "ID更新用户",
        "apiManagerConnID": 0,
        "creator": "李文静",
        "updater": "李文静",
        "apiManager": ""
    },
    "responseHeader": [],
    "headerInfo": [
        {
            "headerName": "Content-Type",
            "headerValue": "application/json",
            "paramNotNull": "0",
            "default": 0,
            "paramType": "0"
        }
    ],
    "authInfo": {
        "status": "0"
    },
    "requestInfo": [
        {
            "paramNotNull": "0",
            "paramType": "0",
            "paramName": "用户ID",
            "paramKey": "id",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "id与name只传一个即可，都传时以id为准",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "用户名",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "name",
            "paramValue": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "外部ID",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": 0,
            "paramKey": "externalId",
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
            "paramKey": "directoryDomain",
            "paramValue": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "13",
            "paramName": "所属组",
            "paramKey": "group",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "可用组织架构的查询接口获取",
            "paramValueList": [],
            "default": "",
            "childList": [
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "op",
                    "paramValue": "set"
                },
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "key",
                    "paramValue": "id"
                },
                {
                    "paramNotNull": "1",
                    "paramType": "0",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "data",
                    "paramValue": "/"
                }
            ]
        },
        {
            "structureID": 1216,
            "updateData": [],
            "childList": []
        },
        {
            "paramNotNull": "1",
            "paramType": "14",
            "paramName": "启用状态：0禁用，1启用",
            "paramKey": "status",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "描述",
            "paramKey": "description",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "密码加密算法类型：'clear'明文，'rsa'非对称加密",
            "paramKey": "pwdModel",
            "paramValue": "clear",
            "paramLimit": "",
            "paramNote": "强烈建议使用'rsa'",
            "paramValueList": [
                {
                    "value": "clear",
                    "valueDescription": "",
                    "paramType": "0"
                }
            ],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "密码",
            "paramKey": "password",
            "paramValue": "♂♀☺♪♫◙♂1",
            "paramLimit": "",
            "paramNote": "如果不修改密码则使用默认值，需要修改密码则使用新密码；如果pwdModel使用'rsa'密码模式，需要对密码进行加密",
            "paramValueList": [
                {
                    "value": "♂♀☺♪♫◙♂1",
                    "valueDescription": "",
                    "paramType": "0"
                }
            ],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "手机号码",
            "paramKey": "phone",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "电子邮件",
            "paramKey": "email",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "0",
            "paramName": "过期时间，13位长度的Unix时间戳，'0'表示永不过期",
            "paramKey": "expiredTime",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        },
        {
            "paramNotNull": "1",
            "paramType": "14",
            "paramName": "继承所属组的应用授权：0不继承，1继承",
            "paramKey": "inheritGroup",
            "paramValue": "",
            "paramLimit": "",
            "paramNote": "",
            "paramValueList": [],
            "default": ""
        }
    ],
    "urlParam": [],
    "restfulParam": [],
    "resultInfo": [
        {
            "responseID": 315,
            "responseCode": "200",
            "responseName": "成功",
            "responseType": 0,
            "paramJsonType": 0,
            "paramList": [
                {
                    "structureID": 1215,
                    "updateData": [],
                    "childList": []
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
    "testCastList": [],
    "mockExpectationList": [],
    "apiType": "http",
    "groupID": 685983,
    "groupName": "",
    "groupDepth": "",
    "apiID": "230",
    "customizeList": [],
    "wsdlContent": "",
    "testData": "",
    "defaultResponseID": 315,
    "mockList": [
        {
            "name": "系统默认期望",
            "source": "高级Mock",
            "url": "/testsdp/api/v3/user/updateById",
            "mockServer": "http://10.65.155.46:11204/mockApi"
        },
        {
            "name": "成功(200)",
            "source": "接口返回",
            "url": "/testsdp/api/v3/user/updateById?responseId=315",
            "mockServer": "http://10.65.155.46:11204/mockApi"
        }
    ],
    "dbFieldObj": {},
    "manager": "",
    "creator": "李文静",
    "updater": "李文静",
    "noticeType": 0,
    "fileList": [],
    "dataStructureList": {
        "1215": {
            "structureID": 1215,
            "structureName": "POST通用返回数据",
            "structureDesc": None,
            "updateTime": "2024-03-19 11:32:57",
            "structureData": [
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "返回码，0 返回成功",
                    "paramKey": "code",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "v8L1ez9bded7be65a22ef5431edc59bad00bc320b8b4f3f"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "13",
                    "paramName": "报文数据主体",
                    "paramKey": "data",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "kWS7IDL8598c39169306adf59d21cf5e089f0887b472cb1"
                },
                {
                    "paramNotNull": "0",
                    "paramType": "0",
                    "paramName": "返回提示信息，与返回码对应",
                    "paramKey": "msg",
                    "paramValue": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "childList": [],
                    "paramID": "4qQJkNp51646445ae11bcaa3be1589b19f179e2ed7ff5e8"
                }
            ],
            "structureType": "15",
            "removed": 0,
            "paramStructIdList": []
        },
        "1216": {
            "structureID": 1216,
            "structureName": "dataSource",
            "structureDesc": "仅外部用户有此参数 数据来源，local、server 从本地配置获取，为 local 从用户目录同步和从认证服务器获取为 server",
            "updateTime": "2024-03-19 11:32:57",
            "structureData": [
                {
                    "paramNotNull": "1",
                    "paramType": "13",
                    "paramName": "",
                    "paramLimit": "",
                    "paramNote": "",
                    "paramValueList": [],
                    "default": 0,
                    "paramKey": "DataSource",
                    "paramValue": "",
                    "childList": [
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "status",
                            "paramValue": "local",
                            "paramID": "ysFNgvG8111915af5f1e3384cb63b768b6986cb12193608",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "displayName",
                            "paramValue": "local",
                            "paramID": "dSyf6wm3c28af6aae6b80799dc433356012b2cea0ebe274",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "email",
                            "paramValue": "local",
                            "paramID": "ptriRRjd96c65bd35c8dc88300530a18a4d7367e7ee9907",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "description",
                            "paramValue": "local",
                            "paramID": "gzEFDb5a47302c1f33cc623781fd41142c2942471ba31a8",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "phone",
                            "paramValue": "local",
                            "paramID": "AiEq3r586e0bd72c145b04967a87657bb7892851613d373",
                            "childList": []
                        },
                        {
                            "paramNotNull": "1",
                            "paramType": "0",
                            "paramName": "",
                            "paramLimit": "",
                            "paramNote": "",
                            "paramValueList": [],
                            "default": 0,
                            "paramKey": "expiredTime",
                            "paramValue": "local",
                            "paramID": "ihDC8F3ce3ff19f0246712fb956bd7a604f6732f27753fe",
                            "childList": []
                        }
                    ],
                    "paramID": "rbPcD2x13439245016cc3d434f6b966b5836a526ec105ad"
                }
            ],
            "structureType": "13",
            "removed": 0,
            "paramStructIdList": []
        }
    }
}

# 续写数据结构合并的模拟数据
RESPONSE_TEXT = """```json
[
    {
        "test_point": "正常场景-按默认参数查询结果集",
        "test_steps": [
            {
                "api_id": 1,
                "api_name": "前置步骤-新增应用分类",
                "api_url": "/api/v1/resource/createResourceGroup",
                "case_data": {
                    "url": "/api/v1/resource/createResourceGroup",
                    "step_type": "api_request",
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
                            "param_key": "name",
                            "param_info": "SSL内部应用",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "description",
                            "param_info": "用于测试的应用分类",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 2,
                "api_name": "前置步骤-新增用户",
                "api_url": "/api/v3/user/create",
                "case_data": {
                    "url": "/api/v3/user/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试用户",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "group",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "op",
                                    "param_info": "set",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "key",
                                    "param_info": "id",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "data",
                                    "param_info": "root",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "password",
                            "param_info": "123456",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 3,
                "api_name": "前置步骤-新增组织架构",
                "api_url": "/api/v3/group/create",
                "case_data": {
                    "url": "/api/v3/group/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试组织架构",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "group",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "op",
                                    "param_info": "set",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "key",
                                    "param_info": "id",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "data",
                                    "param_info": "root",
                                    "child_list": []
                                }
                            ]
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 4,
                "api_name": "前置步骤-新增角色",
                "api_url": "/api/v3/role/create",
                "case_data": {
                    "url": "/api/v3/role/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试角色",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 5,
                "api_name": "主测试步骤-查询应用分类授权-基于名称",
                "api_url": "/api/v3/resourceGroupAssign/queryByName",
                "case_data": {
                    "url": "/api/v3/resourceGroupAssign/queryByName",
                    "step_type": "api_request",
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
                            "param_key": "name",
                            "param_info": "SSL内部应用",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "fieldMode",
                            "param_info": "all",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "sortBy",
                            "param_info": "default",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "entityType",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": "user",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "1",
                                    "param_info": "group",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "2",
                                    "param_info": "band",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "3",
                            "param_key": "pageIndex",
                            "param_info": "1",
                            "child_list": []
                        },
                        {
                            "param_type": "3",
                            "param_key": "pageSize",
                            "param_info": "20",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "count",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageCount",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageSize",
                                    "param_info": "20",
                                    "match_rule": "1",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageIndex",
                                    "param_info": "1",
                                    "match_rule": "1",
                                    "child_list": []
                                },
                                {
                                    "param_key": "data",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": [
                                        {
                                            "param_key": "id",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "name",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "displayName",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "entityType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "userDirectoryId",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "path",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "bandType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "isDeleted",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "serverName",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "dataType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "effectiveTime",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "expireTime",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "description",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "authorisedStatus",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "请求成功",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "traceId",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 6,
                "api_name": "后置步骤-ID删除外部组织架构",
                "api_url": "/api/v3/group/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/group/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[2]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "3",
                            "param_key": "recursive",
                            "param_info": "0",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 7,
                "api_name": "后置步骤-Id批量删除本地用户",
                "api_url": "/api/v3/user/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/user/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[1]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
"""
NEW_RESPONSE_TEXT = """```json
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 8,
                "api_name": "后置步骤-Id批量删除角色",
                "api_url": "/api/v3/role/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/role/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[3]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 9,
                "api_name": "后置步骤-批量删除应用分类",
                "api_url": "/api/v1/resource/deleteResourceGroup",
                "case_data": {
                    "url": "/api/v1/resource/deleteResourceGroup",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[0]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "length",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "name",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            }
        ]
    }
]
```"""
MERGE_RESPONSE_TEXT = """```json
[
    {
        "test_point": "正常场景-按默认参数查询结果集",
        "test_steps": [
            {
                "api_id": 1,
                "api_name": "前置步骤-新增应用分类",
                "api_url": "/api/v1/resource/createResourceGroup",
                "case_data": {
                    "url": "/api/v1/resource/createResourceGroup",
                    "step_type": "api_request",
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
                            "param_key": "name",
                            "param_info": "SSL内部应用",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "description",
                            "param_info": "用于测试的应用分类",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 2,
                "api_name": "前置步骤-新增用户",
                "api_url": "/api/v3/user/create",
                "case_data": {
                    "url": "/api/v3/user/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试用户",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "group",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "op",
                                    "param_info": "set",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "key",
                                    "param_info": "id",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "data",
                                    "param_info": "root",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "password",
                            "param_info": "123456",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 3,
                "api_name": "前置步骤-新增组织架构",
                "api_url": "/api/v3/group/create",
                "case_data": {
                    "url": "/api/v3/group/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试组织架构",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "group",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "op",
                                    "param_info": "set",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "key",
                                    "param_info": "id",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "data",
                                    "param_info": "root",
                                    "child_list": []
                                }
                            ]
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 4,
                "api_name": "前置步骤-新增角色",
                "api_url": "/api/v3/role/create",
                "case_data": {
                    "url": "/api/v3/role/create",
                    "step_type": "api_request",
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
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "name",
                            "param_info": "测试角色",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "id",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 5,
                "api_name": "主测试步骤-查询应用分类授权-基于名称",
                "api_url": "/api/v3/resourceGroupAssign/queryByName",
                "case_data": {
                    "url": "/api/v3/resourceGroupAssign/queryByName",
                    "step_type": "api_request",
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
                            "param_key": "name",
                            "param_info": "SSL内部应用",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "fieldMode",
                            "param_info": "all",
                            "child_list": []
                        },
                        {
                            "param_type": "0",
                            "param_key": "sortBy",
                            "param_info": "default",
                            "child_list": []
                        },
                        {
                            "param_type": "13",
                            "param_key": "entityType",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": "user",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "1",
                                    "param_info": "group",
                                    "child_list": []
                                },
                                {
                                    "param_type": "0",
                                    "param_key": "2",
                                    "param_info": "band",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "3",
                            "param_key": "pageIndex",
                            "param_info": "1",
                            "child_list": []
                        },
                        {
                            "param_type": "3",
                            "param_key": "pageSize",
                            "param_info": "20",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
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
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "count",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageCount",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageSize",
                                    "param_info": "20",
                                    "match_rule": "1",
                                    "child_list": []
                                },
                                {
                                    "param_key": "pageIndex",
                                    "param_info": "1",
                                    "match_rule": "1",
                                    "child_list": []
                                },
                                {
                                    "param_key": "data",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": [
                                        {
                                            "param_key": "id",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "name",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "displayName",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "entityType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "userDirectoryId",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "path",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "bandType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "isDeleted",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "serverName",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "dataType",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "effectiveTime",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "expireTime",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "description",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        },
                                        {
                                            "param_key": "authorisedStatus",
                                            "param_info": "",
                                            "match_rule": "0",
                                            "child_list": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "请求成功",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "traceId",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 6,
                "api_name": "后置步骤-ID删除外部组织架构",
                "api_url": "/api/v3/group/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/group/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[2]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        },
                        {
                            "param_type": "3",
                            "param_key": "recursive",
                            "param_info": "0",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 7,
                "api_name": "后置步骤-Id批量删除本地用户",
                "api_url": "/api/v3/user/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/user/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[1]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 8,
                "api_name": "后置步骤-Id批量删除角色",
                "api_url": "/api/v3/role/bulkDeleteByIdList",
                "case_data": {
                    "url": "/api/v3/role/bulkDeleteByIdList",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[3]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_type": "0",
                            "param_key": "directoryDomain",
                            "param_info": "local",
                            "child_list": []
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            },
            {
                "api_id": 9,
                "api_name": "后置步骤-批量删除应用分类",
                "api_url": "/api/v1/resource/deleteResourceGroup",
                "case_data": {
                    "url": "/api/v1/resource/deleteResourceGroup",
                    "step_type": "api_request",
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
                            "param_type": "12",
                            "param_key": "idList",
                            "param_info": "",
                            "child_list": [
                                {
                                    "param_type": "0",
                                    "param_key": "0",
                                    "param_info": step[0]["response"]["data"]["id"],
                                    "child_list": []
                                }
                            ]
                        }
                    ],
                    "request_type": "2"
                },
                "status_code_verification": {
                    "check_status": true,
                    "status_code": 200
                },
                "response_result_verification": {
                    "check_status": true,
                    "param_match": "json",
                    "json_result_verification": {
                        "result_type": "object",
                        "match_rule": "allElement"
                    },
                    "match_rule": [
                        {
                            "param_key": "code",
                            "param_info": "0",
                            "match_rule": "1",
                            "child_list": []
                        },
                        {
                            "param_key": "data",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": [
                                {
                                    "param_key": "length",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                },
                                {
                                    "param_key": "name",
                                    "param_info": "",
                                    "match_rule": "0",
                                    "child_list": []
                                }
                            ]
                        },
                        {
                            "param_key": "msg",
                            "param_info": "",
                            "match_rule": "0",
                            "child_list": []
                        }
                    ]
                }
            }
        ]
    }
]
```"""

RESPONSE_TEXT_1 = """```json
{
    "match_rule": [
        {
            "param_key": "code",
            "param_info"""

NEW_RESPONSE_TEXT_1 = """```json
            "param_info": "0",
            "match_rule": "1",
            "child_list": []
        }
    ]
}"""

MERGE_RESPONSE_TEXT_1 = """```json
{
    "match_rule": [
        {
            "param_key": "code",
            "param_info": "0",
            "match_rule": "1",
            "child_list": []
        }
    ]
}"""

MOCK_TEST_POINTS = '{\n    "test_points": [\n        "获取单个制品-正常场景-获取XDR产线的制品(即nexus_artifacts_id在1到100之间)",\n        "获取单个制品-正常场景-获取AF产线的制品(即nexus_artifacts_id在101到300之间)",\n        "获取单个制品-异常场景-使用不存在的nexus_artifacts_id(即nexus_artifacts_id不在1到300的范围内)",\n        "获取单个制品-异常场景-使用非法格式的nexus_artifacts_id(即nexus_artifacts_id不是字符串类型)",\n        "获取单个制品-异常场景-使用空值作为nexus_artifacts_id"\n    ]\n}'
