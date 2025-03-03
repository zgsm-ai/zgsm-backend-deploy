#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.statistics_token import StatisticsToken


class StatisticsTokenDao(BaseDao):
    model = StatisticsToken

    @classmethod
    def record_tokens(cls, model_identification: str,
                      application_name: str,
                      user_req_token: int,
                      input_token: int,
                      output_token: int,
                      username: str = None):
        """
        记录请求模型的token数
        :param model_identification: 模型标识
        :param application_name: 应用名称
        :param user_req_token: 用户请求token数
        :param input_token: 请求模型token数
        :param output_token: 模型响应token数
        :param username: 用户名
        """
        data = dict(
            model_identification=model_identification,
            application_name=application_name,
            user_req_token=user_req_token,
            input_token=input_token,
            output_token=output_token,
            username=username,
        )
        cls.create(**data)
