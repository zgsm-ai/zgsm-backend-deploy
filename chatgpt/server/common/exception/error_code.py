#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ERROR_CODE:
    """错误代码
    """
    DEFAULT = 10000

    # 认证相关错误 100001 ~ 110000
    class AUTH:
        # 未登录
        NO_LOGIN = 100001
        # 无权，与403状态码组合时保持唯一
        FORBIDDEN = 100002

    # 资源相关 120000 ~ 130000
    class RESOURCE:
        # 查无资源
        NO_RESOURCE = 120001
        # 查无资源
        NOT_FOUND = 120002
        # 响应头参数错误
        RES_HEADERS_PARAMS_ERROR = 120003

    # 用户输入数据相关 130000 ~ 140000
    class USER_DATA:
        # 字段无效、参数有误
        FIELD_VALID_ERROR = 130001

    # 服务相关 140000 ~ 150000
    class SERVER:
        # 模型错误
        MODEL_ERROR = 140001
        # 参数错误
        PARAMS_ERROR = 140002
        # 第三方请求错误
        REQUEST_ERROR = 140003
        # 操作错误
        OPERATION_ERROR = 140004
        # es 插入错误
        ES_INDEX_ERROR = 140005
        # 切割函数
        FUNCTION_ERROR = 140006
        # 数据操作异常
        DB_ERROR = 140007
        # prompt tokens 过长
        PROMPT_TOKENS_LENGTH = 140008
        # ai返回没有包含代码
        AI_RESPONSE_NO_CODE = 140009

        # gpt异常
        GPT_ERROR = 170002

        # 必填参数缺失异常
        REQUIRE_PARAMS_MISSING_ERROR = 180002

        # 重试异常
        RETRY_ERROR = 180003

        # 参数类型错误异常
        PARAMS_TYPE_ERROR = 180005

        # 手工用例步骤错误
        MANUAL_CASE_ERROR = 180006
