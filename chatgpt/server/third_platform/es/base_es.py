#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 苏德利 16646
    :时间: 2023/3/16 20:23
    :修改者: 苏德利 16646
    :更新时间: 2023/3/16 20:23
"""

import logging
import json
import os
import hashlib
import base64

from config import get_config
from common.exception.exceptions import EsIndexError
from elasticsearch import Elasticsearch
from common.helpers.custom_json_encoder import CustomJSONEncoder

# pylint: disable=no-member
DOC = "_doc"
ES_HOST = get_config().get("es_server")
ES_PASSWORD = os.environ.get("ES_PASSWORD")

logger = None
es = None

def init_es():
    global es
    global logger
    if es is not None:
        return
    logger = logging.getLogger("elasticsearch")
    # 设置日志级别，因为在开发的时候，会将查询结果打印出来，碍眼
    logger.setLevel(logging.INFO)
    logger.info(f"ES_HOST: {ES_HOST}")
    if ES_PASSWORD is None:
        logger.info(f"ES_PASSWORD:")
        es = Elasticsearch(ES_HOST)  
    else:
        logger.info(f"ES_PASSWORD: *****")
        es = Elasticsearch([ES_HOST], http_auth=('elastic', ES_PASSWORD))

def calc_rid(*args) -> str:
    """
    根据参数序列计算具有唯一性的记录ID,只要参数序列不重复,计算出来的HASH值一般就不重复
    """
    # 创建一个SHA-256哈希对象
    sha1_hash = hashlib.sha1()
    for arg in args:
        # 更新哈希对象以包含输入字符串的字节
        sha1_hash.update(arg.encode('utf-8'))
    # 获取十六进制格式的散列值
    hash_bytes = sha1_hash.digest()
    # 将哈希值转换为 Base64 编码
    hash_result = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    # 去掉末尾用作填充的'='
    hash_result = hash_result.rstrip('=')
    return hash_result

class BaseESService:
    def __init__(self):
        init_es()
        self.logger = logger
        self.es = es
        self.index = None
        self._doc = DOC

    def insert(self, obj_dict: dict, id: str = None):
        """更新(或生成)数据到es"""
        try:
            if not ES_HOST:
                return
            if not obj_dict:
                return
            self.es.index(index=self.index, id=id, refresh=True, body=obj_dict, doc_type=self._doc)
        except Exception as err:
            self.logger.error(f"添加es:{self.index}索引出现异常:{str(err)},obj:{obj_dict}")
            raise EsIndexError()

    def bulk_insert(self, objects):
        """
        批量插入  json.dumps(objects, self=CustomJSONEncoder)
        :param objects:
        :return:
        """
        self.logger.info(f"批量插入{len(objects)}条")
        insert_s = list()
        if objects and len(objects):
            for obj in objects:
                insert_s.append(
                    self._gen_update_str(self.index, obj["id"]) + "\n" + json.dumps(obj, cls=CustomJSONEncoder))
            self.es.bulk('\n'.join(insert_s) + '\n', index=self.index, doc_type=self._doc, refresh=True)

    def update_by_id(self, id, update_data):
        try:
            return self.es.update(index=self.index, id=id, body={'doc': update_data})
        except Exception as e:
            self.logger.error(f"修改es:{self.index} id :{id}, update_data:{update_data} 失败：{str(e)}")
            return None

    def _gen_update_str(self, index, doc_id):
        return json.dumps({
            "index": {
                "_index": index,
                "_type": self._doc,
                "_id": doc_id
            }
        })

    def get(self, obj_id):
        """获取es中指定id的数据"""
        try:
            res = self.es.get(index=self.index, doc_type=DOC, id=obj_id)
            return res["_source"] if res else None
        except Exception as ex:
            self.logger.info(f"未找到get_id:{str(ex)}")
            return None

    def delete(self, mid):
        """删除es中指定id数据"""
        try:
            self.es.delete(index=self.index, refresh=True, doc_type=self._doc, id=mid)
            return True
        except Exception as ex:
            self.logger.info(f"未找到delete:{str(ex)}")
            return False
