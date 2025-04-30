from functools import wraps

from flask import request

from common.exception.exceptions import NoResourceError, FieldValidateError

LIST_ARGS_BLACKLIST = ['page', 'per', 'paginate', 'conditions', 'process_query', '_t']


def get_request_kwargs(ignore=[]):
    kwargs = dict()
    for kw in request.args.keys():
        if (kw in LIST_ARGS_BLACKLIST) or (kw in ignore):
            continue
        if request.args.__contains__(kw):
            value = request.args.get(kw)
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
            kwargs[kw] = value
    return kwargs

def filter_fields(kwargs: dict, allow_params: list) -> dict:
    """Filter fields"""
    kwargs = {key: value for key, value in kwargs.items() if key in allow_params}
    return kwargs

def handle_validate(service, methods="create", draft_cache=False):
    def desc(func):
        """
        Validate creation/update fields
        :param service service object
        :param method request method
        :param draft_cache whether to use pipeline cache operation
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if methods == "update":
                if draft_cache is True:
                    pass
                elif kwargs.__contains__('mid') and not service.get_by_id(kwargs['mid']):
                    raise NoResourceError(kwargs['mid'])
                validate, fields = service.validate_update_fields(kwargs.get('mid'), request.json)
            else:
                validate, fields = service.validate_fields(request.json)
            if not validate:
                raise FieldValidateError(fields)
            kwargs['fields'] = fields
            return func(*args, **kwargs)
        return wrapper
    return desc

def handle_paginate(func):
    """
    Handle pagination
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        page = request.args.get('page', default=1, type=int)
        per = request.args.get('per', default=20, type=int)
        paginate = request.args.get('paginate', default='true', type=str)
        if paginate.upper() == 'FALSE':
            kwargs['page'] = None
            kwargs['per'] = None
        else:
            kwargs['page'] = page
            kwargs['per'] = per
        return func(*args, **kwargs)
    return wrapper
