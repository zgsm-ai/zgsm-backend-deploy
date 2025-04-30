#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytz
from datetime import datetime

from third_platform.es.base_es import BaseESService


class CodeCompeltionESservice(BaseESService):
    """Operation record es"""

    def __init__(self):
        super(CodeCompeltionESservice, self).__init__()
        self.index = "code_completion"

    def insert_code_completion(self, data):
        try:
            rid = data['response_id']
            isset = self.es.exists(index=self.index, id=rid)
            if not isset:
                obj_dict = {
                    "id": rid,
                    "username": data['username'],
                    "display_name": data['display_name'],
                    "languageId": data['languageId'].lower(),
                    "prompts": data['prompts'],
                    "code_completions_text": data['code_completions_text'],
                    "code_completions_text_lines": len(data['code_completions_text'].splitlines()),
                    "is_code_completion": data['is_code_completion'],
                    "model": data.get('model', ''),
                    "created_at": datetime.now(pytz.timezone('Asia/Shanghai')),
                    "ide": data.get('ide', ''),
                    "ide_version": data.get('ide_version', ''),
                    "ide_real_version": data.get('ide_real_version', ''),
                    "actual_completions_text": data.get('actual_completions_text', ''),
                    "show_time": data.get('show_time', 0),
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
            else:
                actual_completions_text = data.get('actual_completions_text', '')
                if actual_completions_text:
                    # When the user's real coding data is not empty, only update the coding data field to avoid other fields being changed by the plugin
                    self.update_by_id(id=rid,
                                      update_data={"actual_completions_text": actual_completions_text})
                else:
                    self.update_by_id(id=rid,
                                      update_data={'is_code_completion': data['is_code_completion'],
                                                   'show_time': data.get('show_time', 0)})

        except Exception as e:
            self.logger.error(f"Failed to operate code_completion data in es, error log: {str(e)}")


code_completion_es_service = CodeCompeltionESservice()
