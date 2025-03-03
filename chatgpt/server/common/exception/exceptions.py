#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 15:42
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 15:42
"""
import logging

from flask import current_app

from common.helpers.response_helper import Result
from .error_code import ERROR_CODE

logger = logging.getLogger(__name__)


class CustomException(Exception):
    msg = '错误'
    code = 500
    error_code = ERROR_CODE.DEFAULT
    # 是否要上报到 sentry, 默认上报
    send_to_sentry = True

    @classmethod
    def response(cls, error):
        current_app.logger.error(error, exc_info=True)
        if cls.send_to_sentry:
            try:
                from sentry_sdk import capture_exception
                capture_exception(error)
            except ImportError:
                pass
        return Result.fail(message=str(error), code=cls.code, error_code=cls.error_code)

    @classmethod
    def register(cls, app):
        app.register_error_handler(cls, cls.response)

    def __str__(self):
        if not isinstance(self.msg, str):
            return str(self.msg)
        return self.msg

    def __init__(self, msg=None):
        if msg:
            self.msg = msg


class NoResourceError(CustomException):
    code = 404
    msg = '无此资源'
    error_code = ERROR_CODE.RESOURCE.NO_RESOURCE

    def __init__(self, resource_id=None, label=None):
        if resource_id:
            if label:
                self.msg = f"未找到ID为{resource_id}的{label}数据"
            else:
                self.msg = f"未找到ID为{resource_id}的资源数据"


class FieldValidateError(CustomException):
    code = 403
    msg = '字段校验失败'
    error_code = ERROR_CODE.USER_DATA.FIELD_VALID_ERROR
    send_to_sentry = False


class NoLoginError(CustomException):
    msg = '会话已过期或未登陆，请重新登陆'
    code = 400
    error_code = ERROR_CODE.AUTH.NO_LOGIN
    send_to_sentry = False


class AuthFailError(CustomException):
    msg = '您没有此操作权限，请联系拥有操作权限人员添加权限'
    code = 401
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class NodeAuthFailError(CustomException):
    msg = '您没有此操作权限，请联系维护人添加权限'
    code = 401
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class PermissionFailError(CustomException):
    msg = '您没有此操作权限，请联系管理员添加权限'
    code = 403
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class EsIndexError(CustomException):
    msg = '服务或网络异常'
    code = 500
    error_code = ERROR_CODE.SERVER.ES_INDEX_ERROR


class ModelException(CustomException):
    msg = '服务或网络异常'
    code = 500
    error_code = ERROR_CODE.SERVER.MODEL_ERROR


class OpenAiRequestError(CustomException):
    code = 501
    msg = 'openai服务或网络异常'
    error_code = ERROR_CODE.SERVER.GPT_ERROR
    send_to_sentry = False


class ResourceNotFoundError(CustomException):
    msg = '服务或网络异常'
    code = 404
    error_code = ERROR_CODE.RESOURCE.NOT_FOUND


class ParameterConversionError(CustomException):
    msg = "参数转换异常"
    code = 400
    error_code = ERROR_CODE.SERVER.PARAMS_ERROR


class OperationError(CustomException):
    msg = "操作异常"
    code = 400
    error_code = ERROR_CODE.SERVER.OPERATION_ERROR
    send_to_sentry = False


class RequestError(CustomException):
    msg = "服务或网络异常"
    code = 500
    error_code = ERROR_CODE.SERVER.REQUEST_ERROR


class RequireParamsMissingError(CustomException):
    msg = "必填参数缺失异常"
    code = 500
    error_code = ERROR_CODE.SERVER.REQUIRE_PARAMS_MISSING_ERROR


class RetryError(CustomException):
    msg = "重试异常"
    code = 500
    error_code = ERROR_CODE.SERVER.RETRY_ERROR


class ParamsTypeError(CustomException):
    msg = "参数类型错误异常"
    code = 500
    error_code = ERROR_CODE.SERVER.PARAMS_TYPE_ERROR


class ResHeadersParameterError(CustomException):
    msg = "响应头参数异常"
    code = 400
    error_code = ERROR_CODE.RESOURCE.RES_HEADERS_PARAMS_ERROR


class LockFail(CustomException):
    msg = "加锁失败"
    code = 400
    error_code = ERROR_CODE.SERVER.OPERATION_ERROR


class ForbiddenWordError(CustomException):
    msg = "敏感词汇"
    code = 400
    error_code = ERROR_CODE.USER_DATA.FIELD_VALID_ERROR


class PromptTokensError(CustomException):
    msg = "您需求描述超过了token上限，可减少描述后重试"
    code = 400
    error_code = ERROR_CODE.SERVER.PROMPT_TOKENS_LENGTH

class ManualCaseError(CustomException):
    msg = "用例步骤过于简单，请完善后再进行生成"
    code = 400
    error_code = ERROR_CODE.SERVER.MANUAL_CASE_ERROR


EXCEPTIONS = [
    NoResourceError,
    NoLoginError,
    AuthFailError,
    PermissionFailError,
    EsIndexError,
    ResourceNotFoundError,
    ParameterConversionError,
    OperationError,
    ModelException,
    OpenAiRequestError,
    RequestError,
    FieldValidateError,
    ResHeadersParameterError,
    NodeAuthFailError,
    ForbiddenWordError,
    PromptTokensError,
    ManualCaseError,
]
