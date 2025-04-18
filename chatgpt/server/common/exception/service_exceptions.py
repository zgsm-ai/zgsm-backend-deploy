#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .custom_exception import CustomException


class ResourceNotFoundError(CustomException):
    code = 404
    msg = 'No such resource'
    error_code = 170001
    send_to_sentry = False

    def __init__(self, msg=None, value=None, key="ID", label=None):
        if not msg:
            if value is None or label is None:
                msg = self.msg
            else:
                msg = f"No {label} data found with {key} as {value}"
        super().__init__(msg)


class FieldValidateError(CustomException):
    code = 400
    msg = 'Field validation failed'
    error_code = 170002
    send_to_sentry = False


class NoLoginError(CustomException):
    msg = 'Session has expired or not logged in, please log in again'
    code = 401
    error_code = 170003
    send_to_sentry = False


class UnauthorizedError(CustomException):
    msg = "You do not have permission to perform this operation, please contact someone with permission to add permission"
    code = 403
    error_code = 170004
    send_to_sentry = False


class EsIndexError(CustomException):
    msg = 'ES service or network anomaly'
    code = 500
    error_code = 170005
    send_to_sentry = True


class OpenAiRequestError(CustomException):
    code = 501
    msg = 'openai service or network exception'
    error_code = 170002
    send_to_sentry = False


class ParameterConversionError(CustomException):
    msg = "Parameter conversion exception"
    code = 400
    error_code = 170006
    send_to_sentry = False


class ModelException(CustomException):
    msg = "Database entity exception"
    code = 400
    error_code = 170007
    send_to_sentry = True


class DuplicateError(CustomException):
    msg = "Duplicate data"
    code = 400
    error_code = 170008
    send_to_sentry = False


class NotSupportParamsError(CustomException):
    msg = "Unsupported parameters"
    code = 400
    error_code = 170009
    send_to_sentry = False


class ObjectExistError(CustomException):
    msg = "Object already exists"
    code = 400
    error_code = 170010
    send_to_sentry = False


class RemoteServiceError(CustomException):
    msg = "External service link exception"
    code = 400
    error_code = 170011
    send_to_sentry = True


class UnprocessableEntityError(CustomException):
    msg = "Unprocessable entity"
    code = 422
    error_code = 170012
    send_to_sentry = True


class NexusContentMatchError(CustomException):
    msg = "Artifact content does not match artifact type, please upload a MIME type file or contact Qianliu customer service to turn off the validation function"
    code = 400
    error_code = 170013
    send_to_sentry = True
