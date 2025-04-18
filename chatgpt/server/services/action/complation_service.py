#!/usr/bin/env python
# -*- coding: utf-8 -*-

from services.base_service import BaseService

class CompletionService(BaseService):

    @classmethod
    def validate_fields(cls, fields):
        """Verify the creation data parameters and remove redundant parameters"""
        rules = [
            {'label': 'system_prompt', 'type': list, 'optional': True, 'name': 'System Preset'},
            {'label': 'prompt', 'type': str, 'name': 'prompt'},
            {'label': 'stream', 'type': bool, 'optional': True, 'name': 'Stream Response'},
            {'label': 'conversation_id', 'type': str, 'optional': True, 'name': 'Conversation ID'},
            {'label': 'context_association', 'type': bool, 'optional': True, 'name': 'Enable Context'},
            {'label': 'max_tokens', 'type': int, 'optional': True},
            {'label': 'response_format', 'type': str, 'optional': True},
            {'label': 'replace_forbidden_word', 'type': bool, 'optional': True},  # Whether to automatically replace sensitive words
            {'label': 'context', 'type': str, 'optional': True, 'name': 'Context'}
        ]
        return cls._validate(fields, rules)


class UserGiveFeedbacks(BaseService):
    @classmethod
    def validate_fields(cls, fields):
        rules = [
            {'label': 'action', 'type': str, 'optional': True, 'name': 'action'},
            {'label': 'agent_name', 'type': str, 'optional': False, 'name': 'agent_name'},
            {'label': 'message_id', 'type': str, 'optional': True, 'name': 'Message ID'},
            {'label': 'conversation_id', 'type': str, 'optional': False, 'name': 'Conversation ID'},
            {'label': 'rating', 'type': str, 'optional': True, 'name': 'User Feedback'}
        ]
        return cls._validate(fields, rules)
