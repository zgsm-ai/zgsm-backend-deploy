# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%dT%H:%M:%S.000+0800')
            if isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            if isinstance(obj, Decimal):
                return obj.to_integral_value()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
