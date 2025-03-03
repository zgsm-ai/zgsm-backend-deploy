#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/14 11:38
    :修改者: 苏德利 16646
    :更新时间: 2023/3/14 11:38
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
