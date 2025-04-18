#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import current_app

from common.helpers.response_helper import Result
from .error_code import ERROR_CODE

logger = logging.getLogger(__name__)


class CustomException(Exception):
    msg = 'error'
    code = 500
    error_code = ERROR_CODE.DEFAULT
    # Whether to report to sentry, default is to report
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
    msg = 'No such resource'
    error_code = ERROR_CODE.RESOURCE.NO_RESOURCE

    def __init__(self, resource_id=None, label=None):
        if resource_id:
            if label:
                self.msg = f"No {label} data found with ID {resource_id}"
            else:
                self.msg = f"No resource data found with ID {resource_id}"


class FieldValidateError(CustomException):
    code = 403
    msg = 'Field validation failed'
    error_code = ERROR_CODE.USER_DATA.FIELD_VALID_ERROR
    send_to_sentry = False


class NoLoginError(CustomException):
    msg = 'Session expired or not logged in, please log in again'
    code = 400
    error_code = ERROR_CODE.AUTH.NO_LOGIN
    send_to_sentry = False


class AuthFailError(CustomException):
    msg = 'You do not have permission to perform this operation. Please contact someone with permission to add permission'
    code = 401
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class NodeAuthFailError(CustomException):
    msg = 'You do not have permission to perform this operation. Please contact the maintainer to add permission'
    code = 401
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class PermissionFailError(CustomException):
    msg = 'You do not have permission to perform this operation, please contact the administrator to add permission'
    code = 403
    error_code = ERROR_CODE.AUTH.FORBIDDEN
    send_to_sentry = False


class EsIndexError(CustomException):
    msg = 'Service or network exception'
    code = 500
    error_code = ERROR_CODE.SERVER.ES_INDEX_ERROR


class ModelException(CustomException):
    msg = 'Service or network exception'
    code = 500
    error_code = ERROR_CODE.SERVER.MODEL_ERROR


class OpenAiRequestError(CustomException):
    code = 501
    msg = 'openai service or network exception'
    error_code = ERROR_CODE.SERVER.GPT_ERROR
    send_to_sentry = False


class ResourceNotFoundError(CustomException):
    msg = 'Service or network exception'
    code = 404
    error_code = ERROR_CODE.RESOURCE.NOT_FOUND


class ParameterConversionError(CustomException):
    msg = "Parameter conversion exception"
    code = 400
    error_code = ERROR_CODE.SERVER.PARAMS_ERROR


class OperationError(CustomException):
    msg = "Operation exception"
    code = 400
    error_code = ERROR_CODE.SERVER.OPERATION_ERROR
    send_to_sentry = False


class RequestError(CustomException):
    msg = "Service or network exception"
    code = 500
    error_code = ERROR_CODE.SERVER.REQUEST_ERROR


class RequireParamsMissingError(CustomException):
    msg = "Required parameter missing exception"
    code = 500
    error_code = ERROR_CODE.SERVER.REQUIRE_PARAMS_MISSING_ERROR


class RetryError(CustomException):
    msg = "Retry exception"
    code = 500
    error_code = ERROR_CODE.SERVER.RETRY_ERROR


class ParamsTypeError(CustomException):
    msg = "Parameter type error exception"
    code = 500
    error_code = ERROR_CODE.SERVER.PARAMS_TYPE_ERROR


class ResHeadersParameterError(CustomException):
    msg = "Response header parameter exception"
    code = 400
    error_code = ERROR_CODE.RESOURCE.RES_HEADERS_PARAMS_ERROR


class LockFail(CustomException):
    msg = "Lock failed"
    code = 400
    error_code = ERROR_CODE.SERVER.OPERATION_ERROR


class ForbiddenWordError(CustomException):
    msg = "Sensitive words"
    code = 400
    error_code = ERROR_CODE.USER_DATA.FIELD_VALID_ERROR


class PromptTokensError(CustomException):
    msg = "Your requirement description exceeds the token limit, please reduce the description and try again"
    code = 400
    error_code = ERROR_CODE.SERVER.PROMPT_TOKENS_LENGTH

class ManualCaseError(CustomException):
    msg = "The use case steps are too simple, please improve them before generating"
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
