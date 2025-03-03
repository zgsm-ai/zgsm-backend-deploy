#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 16:58
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 16:58
"""
import base64
import random


def encode_by_base64(message, code_format='utf-8'):
    message = f"{random.randint(100, 20000)}:qianliuapikey:{message}:{random.randint(100, 20000)}"
    message_bytes = message.encode(code_format)
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode(code_format)


def decode_by_base64(base64_message, code_format='utf-8'):
    base64_bytes = base64_message.encode(code_format)
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode(code_format)
