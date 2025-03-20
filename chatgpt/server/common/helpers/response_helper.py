#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    define basic response structure

    :Author: su deli 16646
    :Time: 2023/3/14 15:45
    :Modifier: su deli 16646
    :UpdateTime: 2023/3/14 15:45
"""
from typing import Iterator
from flask import jsonify, make_response, request, Response, stream_with_context
from peewee import ModelSelect, Model


class Result:

    @classmethod
    def message(cls, state_str="success"):
        method_name = request.method
        if "GET" == method_name:
            return f"get {state_str}"
        elif "POST" == method_name:
            return f"operate {state_str}"
        elif "DELETE" == method_name:
            return f"delete {state_str}"
        elif "PUT" == method_name:
            return f"update {state_str}"
        return ""

    @classmethod
    def success(cls, data=None, total=None, message=None, code=200, info_code=None, **kwargs):
        # solve the error of empty data processing
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
            "message": message if message else cls.message("failed"),
            "data": data,
            "success": False
        }
        if info_code:
            resp.update(code=info_code)
        resp.update(kwargs)
        return make_response(jsonify(resp), code)

    @classmethod
    def fail_404(cls, msg='No such resource', data=None, code=404):
        resp = make_response(jsonify({
            "msg": msg,
            "data": data,
            "success": False
        }), code)
        return resp

    @classmethod
    def stream_response(cls, result: Iterator[str], is_use_sse_struct: bool = False):
        """
        return streaming response, streaming output result sse protocol encapsulation, streaming output data to client
        @param result: iterator
        @param is_use_sse_struct: whether to use sse protocol data structure
        @return: http response
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
        generate chunk assembled into sse protocol
        @param result:
        @return:
        """
        # message format of sse protocol
        message_chunk = "data: {}\n\n"
        for res in result:
            yield message_chunk.format(res)
