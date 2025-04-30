#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

from common.helpers.custom_permission import PermissionChecker
from common.helpers.response_helper import Result
from controllers.base import handle_validate, handle_paginate, get_request_kwargs
from services.system.prompt_square_service import prompt_square_service, PromptSquareService, prompt_square_hot_service, \
    PromptSquareHotService

permission_check = PermissionChecker.check_is_admin_or_creator

prompt_square = Blueprint('prompt_square', __name__)


@prompt_square.route("", methods=['GET'])
@handle_paginate
def get(page, per):
    """
    Prompt sharing data
    Query: get api/prompt_square
        - Supports fuzzy title search
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    search_kw = get_request_kwargs()
    query, total = prompt_square_service.list(page=page, per=per, **search_kw)
    return Result.success(message='Get Success', data=query, total=total)


@prompt_square.route("", methods=['POST'])
@handle_validate(PromptSquareService)
def post(fields):
    """
    Prompt sharing data
    Create new
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    resp = prompt_square_service.create(**fields)
    return Result.success(message='Get Success', data=resp)


@prompt_square.route("/<int:mid>", methods=['PUT'])
@permission_check(PromptSquareService)
@handle_validate(PromptSquareService, methods='update')
def put(mid, fields):
    """
    Prompt sharing data
    Update: put api/prompt_square/{mid}
        - Permission requires admin or creator
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    resp = prompt_square_service.update(mid, **fields)
    return Result.success(message='Update Success', data=resp)


@prompt_square.route("/<int:mid>", methods=['DELETE'])
@permission_check(PromptSquareService)
def delete(mid):
    """
    Prompt sharing data
    Delete: delete api/prompt_square/{mid}
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    PromptSquareService.delete_by_id(mid)
    return Result.success()


@prompt_square.route("/<int:mid>/hot", methods=['PUT'])
@handle_validate(PromptSquareHotService, methods='update')
def hot_put(mid, fields):
    """
    Prompt sharing data
    Update: put api/prompt_square/{mid}/hot
        - Increase popularity by 1
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    resp = prompt_square_hot_service.update(mid, **fields)
    return Result.success(message='Update Success', data=resp)


@prompt_square.route("/title", methods=['GET'])
@handle_paginate
def title_get(page, per):
    """
    Prompt sharing data
    Query fuzzy title search: get api/prompt_square/title
        - Returns partial fields
    ---
    tags:
      - system
    responses:
      200:
        res: Result
    """
    search_kw = get_request_kwargs()
    if not search_kw.get('ordering'):
        search_kw['ordering'] = '-hot,title'
    include_fields = ('id', 'title', 'prompt', 'hot')  # Specify returned fields

    query, total = prompt_square_service.list(page=page, per=per, include_fields=include_fields, **search_kw)
    return Result.success(message='Get Success', data=query, total=total)
