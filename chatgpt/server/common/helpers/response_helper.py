#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    定义基本的response响应结构

    :作者: 苏德利 16646
    :时间: 2023/3/14 15:45
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 15:45
"""
from typing import Iterator
from flask import jsonify, make_response, request, Response, stream_with_context
from peewee import ModelSelect, Model


class Result:

    @classmethod
    def message(cls, state_str="成功"):
        method_name = request.method
        if "GET" == method_name:
            return f"获取{state_str}"
        elif "POST" == method_name:
            return f"操作{state_str}"
        elif "DELETE" == method_name:
            return f"删除{state_str}"
        elif "PUT" == method_name:
            return f"更新{state_str}"
        return ""

    @classmethod
    def success(cls, data=None, total=None, message=None, code=200, info_code=None, **kwargs):
        # 解决空数据处理错误问题
        if isinstance(data, ModelSelect):
            if data:
                data = [item.dict() for item in data]
            else:
                data = []
        elif isinstance(data, Model):
            data = data.dict()
        resp = {
            "message": message if message else cls.message(),
            'data': data,
            "success": True
        }
        if total is not None:
            resp['total'] = total
        if info_code is not None:
            resp['code'] = info_code
        resp.update(kwargs)
        return make_response(jsonify(resp), code)

    @classmethod
    def fail(cls, data=None, message=None, code=400, info_code=None, **kwargs):
        resp = {
            "message": message if message else cls.message("失败"),
            "data": data,
            "success": False
        }
        if info_code:
            resp.update(code=info_code)
        resp.update(kwargs)
        return make_response(jsonify(resp), code)

    @classmethod
    def fail_404(cls, msg='无此资源', data=None, code=404):
        resp = make_response(jsonify({
            "msg": msg,
            "data": data,
            "success": False
        }), code)
        return resp

    @classmethod
    def stream_response(cls, result: Iterator[str], is_use_sse_struct: bool = False):
        """
        返回流式响应,流式输出结果sse协议封装，将数据流式输出到客户端
        @param result: 迭代器
        @param is_use_sse_struct: 是否使用sse协议数据结构
        @return: http 响应
        """
        if is_use_sse_struct:
            data_chunk = cls.gen_sse_data_chunk(result)
        else:
            data_chunk = result
        return Response(stream_with_context(data_chunk), mimetype='text/event-stream', headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })

    @staticmethod
    def gen_sse_data_chunk(result: Iterator) -> Iterator[str]:
        """
        生组装成sse协议的chunk
        @param result:
        @return:
        """
        # sse协议的message格式
        message_chunk = "data: {}\n\n"
        for res in result:
            yield message_chunk.format(res)
