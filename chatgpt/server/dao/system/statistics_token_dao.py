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
        Record the number of tokens requested by the model
        :param model_identification: Model identifier
        :param application_name: Application name
        :param user_req_token: Number of tokens in user request
        :param input_token: Number of tokens requested by the model
        :param output_token: Number of tokens in model response
        :param username: Username
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
