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
        Record the number of tokens for the requested model
        :param model_identification: Model identification
        :param application_name: Application name
        :param user_req_token: Number of user request tokens
        :param input_token: Number of request model tokens
        :param output_token: Number of model response tokens
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
