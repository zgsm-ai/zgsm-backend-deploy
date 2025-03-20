#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, IntegerField

logger = logging.getLogger(__name__)


class StatisticsToken(BaseModel):
    """Model uses token number statistics"""

    class Meta:
        table_name = 'statistics_token'

    application_name = CharField(verbose_name='Application Name')
    username = CharField(null=True, verbose_name='User')
    model_identification = CharField(verbose_name='Model Identification')
    user_req_token = IntegerField(verbose_name='Model Name')  # The number of tokens requested by the user, including (system, user)
    input_token = IntegerField(verbose_name='Request Model Input Token')  # The number of tokens for the requested model, including (system, user, context)
    output_token = IntegerField(verbose_name='Request Model Output Token')  # The number of tokens for the model response

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
