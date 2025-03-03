#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.base_model import BaseModel
from peewee import CharField, IntegerField

logger = logging.getLogger(__name__)


class StatisticsToken(BaseModel):
    """模型使用token数统计"""

    class Meta:
        table_name = 'statistics_token'

    application_name = CharField(verbose_name='应用名称')
    username = CharField(null=True, verbose_name='用户')
    model_identification = CharField(verbose_name='模型标识')
    user_req_token = IntegerField(verbose_name='模型名称')  # 用户请求的token数，包含（system、user）
    input_token = IntegerField(verbose_name='请求模型输入token')  # 请求模型的token数，包含（system、user、上下文）
    output_token = IntegerField(verbose_name='请求模型输出token')  # 模型响应的token数

    def dict(self, *args, **kwargs):
        data = super().dict()
        return data
