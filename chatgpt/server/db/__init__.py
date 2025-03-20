#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Brief introduction

    :Author: SudeLi 16646
    :Time: 2023/3/14 11:38
    :Modifier: SudeLi 16646
    :UpdateTime: 2023/3/14 11:38
"""
from peewee import Proxy
from playhouse.db_url import connect
from config import conf


class CustomProxy(Proxy):
    def init_database(self):
        database = connect(conf.get('database_uri'))
        self.initialize(database)

    def init_app(self, app):
        self.init_database()

        @app.before_request
        def before():
            """ comment by lyb """
            # self.obj.connect()
            pass

        @app.teardown_request
        def teardown(response):
            if not self.obj.is_closed():
                self.obj.close()
            return response


db = CustomProxy()
