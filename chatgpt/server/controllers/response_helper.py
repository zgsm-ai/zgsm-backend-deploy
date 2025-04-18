#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from typing import Iterator
from flask import jsonify, make_response, request, Response, stream_with_context


class Result:
    @classmethod
    def message(cls, state_str="success"):
        method_name = request.method
        if "GET" == method_name:
            return f"Get {state_str}"
        elif "POST" == method_name:
            return f"Operate {state_str}"
        elif "DELETE" == method_name:
            return f"Delete {state_str}"
        elif "PUT" == method_name:
            return f"Update {state_str}"
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
            "message": message if message else cls.message("Failed"),
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
        Return streaming response, stream output results using SSE protocol encapsulation, stream data to the client
        @param result: iterator
        @return: http response
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
        Generate and assemble SSE protocol chunks
        @param result:
        @return:
        """
        # sse protocol message format
        message_chunk = "data: {}\n\n"
        for res in result:
            yield message_chunk.format(res)
