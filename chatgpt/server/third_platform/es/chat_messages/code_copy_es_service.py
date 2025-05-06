#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from third_platform.es.base_es import BaseESService, calc_rid


class CodeCopyESservice(BaseESService):
    """Operation record es"""

    def __init__(self):
        super(CodeCopyESservice, self).__init__()
        self.index = "code_copy"

    def _calc_rid(self, data):
        return calc_rid(data['display_name'], data['code_copy'], data['action'])

    def insert_code_completion(self, data):
        try:
            # Same user, same code segment, same action
            rid = self._calc_rid(data)

            isset = self.es.exists(index=self.index, id=rid)
            if not isset:
                obj_dict = {
                    "id": rid,
                    "display_name": data['display_name'],
                    "languageId": data['language'].lower(),
                    "code_copy": data['code_copy'],
                    "code_copy_text_lines": len(data['code_copy'].splitlines()),
                    "created_at": datetime.now(pytz.timezone('Asia/Shanghai')),
                    "ide": data.get('ide', ''),
                    "ide_version": data.get('ide_version', ''),
                    "ide_real_version": data.get('ide_real_version', ''),
                    "action": data.get('action', ''),
                    "is_select": data.get('is_select', False)
                }
                # Add an extra_kwargs field in dict format, all parameters are saved, and future new fields can be placed here.
                if 'extra_kwargs' in data.keys():
                    for key, value in data['extra_kwargs'].items():
                        try:
                            # There may be ISO format strings, try to parse the string into a datetime object
                            value = datetime.fromisoformat(value)
                        except Exception:
                            # If parsing fails, store in the original format
                            pass
                        obj_dict[key] = value

                # Add server_extra_kwargs server extension fields
                if 'server_extra_kwargs' in data.keys():
                    for key, value in data['server_extra_kwargs'].items():
                        try:
                            # There may be ISO format strings, try to parse the string into a datetime object
                            value = datetime.fromisoformat(value)
                        except Exception:
                            # If parsing fails, store in the original format
                            pass
                        obj_dict[key] = value

                self.insert(obj_dict, id=rid)

        except Exception as e:
            self.logger.error(f"Failed to operate {self.index} data in es, error log: {str(e)}")


code_copy_es_service = CodeCopyESservice()
