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
from third_platform.es.base_es import BaseESService, calc_rid


class CodeCopyESservice(BaseESService):
    """操作记录es"""

    def __init__(self):
        super(CodeCopyESservice, self).__init__()
        self.index = "code_copy"

    def _calc_rid(self, data):
        return calc_rid(data['display_name'], data['code_copy'], data['action'])

    def insert_code_completion(self, data):
        try:
            # 同一个用户的 同一段代码 同一个动作
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

        except Exception as e:
            self.logger.error(f"es 操作 {self.index} 数据失败，失败日志： {str(e)}")


code_copy_es_service = CodeCopyESservice()
