#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author  : 刘鹏z10807
@Date    : 2023/5/15 15:45
"""

from services.base_service import BaseService

class CompletionService(BaseService):

    @classmethod
    def validate_fields(cls, fields):
        """校验创建数据参数，去除冗余参数"""
        """Verify the creation data parameters and remove redundant parameters"""
        rules = [
            {'label': 'system_prompt', 'type': list, 'optional': True, 'name': '系统预设'},
            {'label': 'prompt', 'type': str, 'name': 'prompt'},
            {'label': 'stream', 'type': bool, 'optional': True, 'name': '是否流式响应'},
            {'label': 'conversation_id', 'type': str, 'optional': True, 'name': '对话流id'},
            {'label': 'context_association', 'type': bool, 'optional': True, 'name': '是否开启上下文'},
            {'label': 'max_tokens', 'type': int, 'optional': True},
            {'label': 'response_format', 'type': str, 'optional': True},
            {'label': 'replace_forbidden_word', 'type': bool, 'optional': True},  # 是否自动替换敏感词
            {'label': 'replace_forbidden_word', 'type': bool, 'optional': True},  # Whether to automatically replace sensitive words
            {'label': 'context', 'type': str, 'optional': True, 'name': '上下文'}
        ]
        return cls._validate(fields, rules)


class UserGiveFeedbacks(BaseService):
    @classmethod
    def validate_fields(cls, fields):
        rules = [
            {'label': 'action', 'type': str, 'optional': True, 'name': 'action'},
            {'label': 'agent_name', 'type': str, 'optional': False, 'name': 'agent_name'},
            {'label': 'message_id', 'type': str, 'optional': True, 'name': '消息id'},
            {'label': 'conversation_id', 'type': str, 'optional': False, 'name': '对话流id'},
            {'label': 'rating', 'type': str, 'optional': True, 'name': '用户反馈'}
        ]
        return cls._validate(fields, rules)
