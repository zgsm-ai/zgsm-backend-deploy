#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    平台服务相关的错误
    error_code： 170 开头

    :作者: 苏德利 16646
    :时间: 2023/3/16 20:40
    :修改者: 苏德利 16646
    :更新时间: 2023/3/16 20:40
"""

from .custom_exception import CustomException


class ResourceNotFoundError(CustomException):
    code = 404
    msg = '无此资源'
    error_code = 170001
    send_to_sentry = False

    def __init__(self, msg=None, value=None, key="ID", label=None):
        if not msg:
            if value is None or label is None:
                msg = self.msg
            else:
                msg = f"未找到{key}为{value}的{label}数据"
        super().__init__(msg)


class FieldValidateError(CustomException):
    code = 400
    msg = '字段校验失败'
    error_code = 170002
    send_to_sentry = False


class NoLoginError(CustomException):
    msg = '会话已过期或未登陆，请重新登陆'
    code = 401
    error_code = 170003
    send_to_sentry = False


class UnauthorizedError(CustomException):
    msg = "您没有此操作权限，请联系拥有操作权限人员添加权限"
    code = 403
    error_code = 170004
    send_to_sentry = False


class EsIndexError(CustomException):
    msg = 'ES服务或网络异常'
    code = 500
    error_code = 170005
    send_to_sentry = True


class OpenAiRequestError(CustomException):
    code = 501
    msg = 'openai服务或网络异常'
    error_code = 170002
    send_to_sentry = False


class ParameterConversionError(CustomException):
    msg = "参数转换异常"
    code = 400
    error_code = 170006
    send_to_sentry = False


class ModelException(CustomException):
    msg = "数据库实体出现异常"
    code = 400
    error_code = 170007
    send_to_sentry = True


class DuplicateError(CustomException):
    msg = "重复的数据"
    code = 400
    error_code = 170008
    send_to_sentry = False


class NotSupportParamsError(CustomException):
    msg = "不支持的参数"
    code = 400
    error_code = 170009
    send_to_sentry = False


class ObjectExistError(CustomException):
    msg = "对象已存在"
    code = 400
    error_code = 170010
    send_to_sentry = False


class RemoteServiceError(CustomException):
    msg = "外部服务链接异常"
    code = 400
    error_code = 170011
    send_to_sentry = True


class UnprocessableEntityError(CustomException):
    msg = "不可处理的实体"
    code = 422
    error_code = 170012
    send_to_sentry = True


class NexusContentMatchError(CustomException):
    msg = "制品内容与制品类型不匹配(Artifact content does not match artifact type)，请上传MIME类型文件，或找千流客服关闭校验功能"
    code = 400
    error_code = 170013
    send_to_sentry = True
