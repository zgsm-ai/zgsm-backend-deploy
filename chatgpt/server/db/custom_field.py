import json
from datetime import datetime

from peewee import TextField


class CustomEncoding(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
        except TypeError:
            pass
        return json.JSONEncoder.default(self, obj)


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value, ensure_ascii=False, cls=CustomEncoding)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)
        else:
            return {}
