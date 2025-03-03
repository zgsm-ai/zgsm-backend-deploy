#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/3/27 10:55
"""

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
    prompt分享数据
    查询: get api/prompt_square
        - 支持标题模糊查询
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    search_kw = get_request_kwargs()
    query, total = prompt_square_service.list(page=page, per=per, **search_kw)
    return Result.success(message='获取成功', data=query, total=total)


@prompt_square.route("", methods=['POST'])
@handle_validate(PromptSquareService)
def post(fields):
    """
    prompt分享数据
    新增
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    resp = prompt_square_service.create(**fields)
    return Result.success(message='获取成功', data=resp)


@prompt_square.route("/<int:mid>", methods=['PUT'])
@permission_check(PromptSquareService)
@handle_validate(PromptSquareService, methods='update')
def put(mid, fields):
    """
    prompt分享数据
    修改：put api/prompt_square/{mid}
        - 权限需要超管或创建者
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    resp = prompt_square_service.update(mid, **fields)
    return Result.success(message='更新成功', data=resp)


@prompt_square.route("/<int:mid>", methods=['DELETE'])
@permission_check(PromptSquareService)
def delete(mid):
    """
    prompt分享数据
    删除：delete api/prompt_square/{mid}
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    PromptSquareService.delete_by_id(mid)
    return Result.success()


@prompt_square.route("/<int:mid>/hot", methods=['PUT'])
@handle_validate(PromptSquareHotService, methods='update')
def hot_put(mid, fields):
    """
    prompt分享数据
    修改：put api/prompt_square/{mid}/hot
        - 热度+1
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    resp = prompt_square_hot_service.update(mid, **fields)
    return Result.success(message='更新成功', data=resp)


@prompt_square.route("/title", methods=['GET'])
@handle_paginate
def title_get(page, per):
    """
    prompt分享数据
    查询 标题模糊查询：get api/prompt_square/title
        - 返回部分字段
    ---
    tags:
      - system
    responses:
      200:
        res: 结果
    """
    search_kw = get_request_kwargs()
    if not search_kw.get('ordering'):
        search_kw['ordering'] = '-hot,title'
    include_fields = ('id', 'title', 'prompt', 'hot')  # 指定返回字段

    query, total = prompt_square_service.list(page=page, per=per, include_fields=include_fields, **search_kw)
    return Result.success(message='获取成功', data=query, total=total)
