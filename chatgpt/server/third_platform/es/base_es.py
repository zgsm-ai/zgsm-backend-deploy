#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    # Set log level, because during development, the query results are printed out, which is distracting
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
    Calculate a unique record ID based on the parameter sequence, as long as the parameter sequence is not repeated, the calculated HASH value is generally not repeated
    """
    # Create a SHA-256 hash object
    sha1_hash = hashlib.sha1()
    for arg in args:
        # Update the hash object to include the bytes of the input string
        sha1_hash.update(arg.encode('utf-8'))
    # Get the hash value in hexadecimal format
    hash_bytes = sha1_hash.digest()
    # Convert the hash value to Base64 encoding
    hash_result = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    # Remove the '=' used as padding at the end
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
        """Update (or generate) data to es"""
        try:
            if not ES_HOST:
                return
            if not obj_dict:
                return
            self.es.index(index=self.index, id=id, refresh=True, body=obj_dict, doc_type=self._doc)
        except Exception as err:
            self.logger.error(f"Error adding to es:{self.index} index:{str(err)},obj:{obj_dict}")
            raise EsIndexError()

    def bulk_insert(self, objects):
        """
        Bulk insertion  json.dumps(objects, self=CustomJSONEncoder)
        :param objects:
        :return:
        """
        self.logger.info(f"Bulk inserting {len(objects)} items")
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
            self.logger.error(f"Error modifying es:{self.index} id :{id}, update_data:{update_data} failed:{str(e)}")
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
        """Get data with specified id from es"""
        try:
            res = self.es.get(index=self.index, doc_type=DOC, id=obj_id)
            return res["_source"] if res else None
        except Exception as ex:
            self.logger.info(f"get_id not found:{str(ex)}")
            return None

    def delete(self, mid):
        """Delete data with specified id from es"""
        try:
            self.es.delete(index=self.index, refresh=True, doc_type=self._doc, id=mid)
            return True
        except Exception as ex:
            self.logger.info(f"delete not found:{str(ex)}")
            return False
