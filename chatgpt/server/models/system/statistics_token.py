#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, IntegerField

logger = logging.getLogger(__name__)


class StatisticsToken(BaseModel):
    """Model token usage statistics"""

    class Meta:
        table_name = 'statistics_token'

    application_name = CharField(verbose_name='Application Name')
    username = CharField(null=True, verbose_name='User')
    model_identification = CharField(verbose_name='Model Identifier')
    user_req_token = IntegerField(verbose_name='Model Name')  # Number of tokens in user request, including (system, user)
    input_token = IntegerField(verbose_name='Request Model Input Tokens')  # Number of tokens in model request, including (system, user, context)
    output_token = IntegerField(verbose_name='Request Model Output Tokens')  # Number of tokens in model response

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
