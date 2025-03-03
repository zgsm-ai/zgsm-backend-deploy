#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：范立伟33139
@Date    ：2023/3/16 14:17
"""
from typing import Iterator
from flask import jsonify, make_response, request, Response, stream_with_context


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
        resp = {
            "message": message if message else cls.message(),
            "data": data,
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
    def import_success(cls, data):
        return make_response(jsonify({
            "jsonData": {
                "success": True,
                "data": data
            }
        }))

    @classmethod
    def import_fail(cls, err):
        return make_response(jsonify({
            "jsonData": {
                "success": False,
                "data": None,
                "msg": str(err)
            }
        }))

    @classmethod
    def stream_response(cls, result: Iterator[str]):
        """
        返回流式响应,流式输出结果sse协议封装，将数据流式输出到客户端
        @param result: 迭代器
        @return: http 响应
        """
        data_chunk = cls.gen_data_chunk(result)

        return Response(stream_with_context(data_chunk), mimetype='text/event-stream', headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        })

    @staticmethod
    def gen_data_chunk(result: Iterator) -> Iterator[str]:
        """
        生组装成sse协议的chunk
        @param result:
        @return:
        """
        # sse协议的message格式
        message_chunk = "data: {}\n\n"
        for res in result:
            yield message_chunk.format(res)
