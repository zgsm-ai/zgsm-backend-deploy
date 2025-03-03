#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/16 20:33
    :修改者: 苏德利 16646
    :更新时间: 2023/3/16 20:33
"""

import pytz
from datetime import datetime

from third_platform.es.base_es import BaseESService


class CodeCompeltionESservice(BaseESService):
    """操作记录es"""

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
                # 新增一个extra_kwargs字段, 格式为dict, 里面的所有参数都保存, 未来新加的字段都可以放这里面。
                if 'extra_kwargs' in data.keys():
                    for key, value in data['extra_kwargs'].items():
                        try:
                            # 可能存在iso格式字符串，尝试将字符串解析为 datetime 对象
                            value = datetime.fromisoformat(value)
                        except Exception:
                            # 只要解析失败，就直接按源格式存储
                            pass
                        obj_dict[key] = value

                # 新增 server_extra_kwargs 服务端拓展字段
                if 'server_extra_kwargs' in data.keys():
                    for key, value in data['server_extra_kwargs'].items():
                        try:
                            # 可能存在iso格式字符串，尝试将字符串解析为 datetime 对象
                            value = datetime.fromisoformat(value)
                        except Exception:
                            # 只要解析失败，就直接按源格式存储
                            pass
                        obj_dict[key] = value
                self.insert(obj_dict, id=rid)
            else:
                actual_completions_text = data.get('actual_completions_text', '')
                if actual_completions_text:
                    # 当用户真实编码数据为非空时，只更新编码数据字段，避免其他字段被插件更改
                    self.update_by_id(id=rid,
                                      update_data={"actual_completions_text": actual_completions_text})
                else:
                    self.update_by_id(id=rid,
                                      update_data={'is_code_completion': data['is_code_completion'],
                                                   'show_time': data.get('show_time', 0)})

        except Exception as e:
            self.logger.error(f"es 操作 code_completion数据失败，失败日志： {str(e)}")


code_completion_es_service = CodeCompeltionESservice()
