#!/usr/bin/env python3
# -*- coding: utf8 -*-
import json
from datetime import timedelta
from functools import wraps

from config import get_config

try:
    import cPickle as pickle
except (ImportError, ModuleNotFoundError):
    import pickle

import redis

from .exception import (CacheNoConnectionError, CacheKeyError, CacheValueError)


def handle_value(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        raise_none = default = None
        try:
            raise_none = kwargs.pop('raise_none')
            default = kwargs.pop('default')
        except KeyError:
            pass
        original_value = func(self, *args, **kwargs)
        return self.value_handler(original_value,
                                  raise_none=raise_none,
                                  default=default)

    return wrapper


def handle_key(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        required_args_count = func.__code__.co_argcount - 1
        if len(args) < required_args_count:
            raise CacheKeyError('Wrong number of arguments for Caching.')
        keys = args[:len(args) - required_args_count + 1]
        args = args[len(args) + 1 - required_args_count:]
        if bool([k for k in keys
                 if (not isinstance(k, str)) and (not isinstance(k, int))]):
            raise CacheKeyError('Invalid Key')
        return func(self, *[self.make_key(keys), *args], **kwargs)

    return wrapper


class BaseCache:
    pools_dict = {}

    def __init__(self, namespace=None, serializer='pickle', url=None):
        self.url = url
        self.pool = None
        self.connection = None
        self._create_pool()
        self.namespace = namespace
        if serializer == 'json':
            self.serializer = json
        else:
            self.serializer = pickle

        # 确保每次都是连接同一个连接池
        if not self.pool:
            raise CacheNoConnectionError
        if not self.connection:
            self.connection = redis.Redis(connection_pool=self.pool)

    def _create_pool(self):
        if not self.url:
            self.url = get_config().get('redis_url')
        pool = BaseCache.pools_dict.get(self.url)
        if pool:
            self.pool = pool
        else:
            self.pool = redis.ConnectionPool.from_url(self.url)
            BaseCache.pools_dict[self.url] = self.pool

    def serialize(self, value):
        """Serialization"""
        if isinstance(value, dict):
            # Store dictionary type as map
            # return {k: self.serializer.dumps(v) for k, v in value.items()}
            return self.serializer.dumps(value)
        else:
            return self.serializer.dumps(value)

    def deserialize(self, value):
        """Deserialization"""
        if isinstance(value, dict):
            # Key needs to be encoded as utf8, otherwise it comes back as bytes
            return {k.decode('utf-8'): self.serializer.loads(v) for k, v in value.items()}
        elif isinstance(value, (list, set)):
            return [self.serializer.loads(v) for v in value]
        else:
            return self.serializer.loads(value)

    def make_key(self, *args):
        """Construct cache key"""
        if len(args) < 1:
            raise CacheKeyError('missing key(s)')
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        return ':'.join([str(i) for i in [self.namespace, *args] if i is not None])

    def value_handler(self, value, **kwargs):
        if value is None:
            if kwargs.get('raise_none'):
                raise CacheKeyError
            else:
                return kwargs.get('default', None)
        return self.deserialize(value)

    @handle_value
    @handle_key
    def get(self, name):
        return self.connection.get(name)

    @handle_key
    def keys(self, pattern):
        return list(map(lambda k: k.decode("utf-8"), self.connection.keys(pattern=pattern)))

    @handle_value
    @handle_key
    def hgetall(self, name):
        return self.connection.hgetall(name)

    @handle_value
    @handle_key
    def hvals(self, name):
        return self.connection.hvals(name)

    @handle_key
    def hkeys(self, name):
        return self.connection.hkeys(name)

    @handle_key
    def hlen(self, name):
        return self.connection.hlen(name)

    @handle_key
    def hdel(self, name, key):
        return self.connection.hdel(name, key)

    @handle_value
    @handle_key
    def hget(self, name, key):
        return self.connection.hget(name, key)

    def __getitem__(self, key):
        args = [*key] if isinstance(key, tuple) else [key]
        return self.get(*args, raise_none=True)

    @handle_key
    def set(self, name, value, *args, **kwargs):
        return self.connection.set(name, self.serialize(value), *args, **kwargs)

    @handle_key
    def hmset(self, name, mapping):
        if not isinstance(mapping, dict):
            raise CacheValueError
        return self.connection.hmset(name, self.serialize(mapping))

    @handle_key
    def hset(self, name, key, value):
        return self.connection.hset(name, key, self.serialize(value))

    def __setitem__(self, key, value):
        args = [*key] if isinstance(key, tuple) else [key]
        return self.set(*args, value)

    @handle_key
    def delete(self, key):
        """
        Delete one cache with specific name
        """
        return self.connection.delete(key)

    remove = delete

    @handle_key
    def expire(self, key, seconds):
        """
        Set expiration time (in seconds)
        """
        return self.connection.expire(key, timedelta(seconds=seconds))

    def clear(self, rule=None):
        """
        Clear cache under the current namespace
        """
        if not rule:
            rule = "*"
        keys = list(self.connection.scan_iter(match=self.make_key(rule)))
        if keys:
            self.connection.delete(*keys)

    def flushall(self):
        """
        清空全部缓存
        """
        print('清空全部缓存')
        self.connection.flushall()

    @handle_key
    def push(self, key, value, rpush=True):
        if rpush:
            self.connection.rpush(key, value)
        else:
            self.connection.lpush(key, value)

    @handle_value
    @handle_key
    def pop(self, key, rpop=False):
        if rpop:
            return self.connection.rpop(key)
        else:
            return self.connection.lpop(key)

    @handle_value
    @handle_key
    def blpop(self, key, timeout):
        """
        定义函数blpop, 用于从Redis中弹出左侧第一个元素
        会阻塞redis动作，直到超时时间后弹出
        args:
            key: 要操作的键
            timeout: 超时时间，单位为秒
        return:
            被弹出的元素
        """
        return self.connection.blpop(key, timeout=timeout)

    @handle_key
    def sadd(self, key, value):
        return self.connection.sadd(key, *value)

    @handle_value
    @handle_key
    def smembers(self, key):
        return self.connection.smembers(key)

    @handle_key
    def sismember(self, key, value):
        return self.connection.sismember(key, value)

    @handle_key
    def srem(self, key, value):
        return self.connection.srem(key, *value)

    @handle_key
    def scard(self, key):
        return self.connection.scard(key)

    @handle_key
    def llen(self, key):
        return self.connection.llen(key)

    @handle_value
    @handle_key
    def lindex(self, key, index):
        return self.connection.lindex(key, index)

    @handle_value
    @handle_key
    def lrange(self, key, start, end):
        return self.connection.lrange(key, start, end)

    @handle_key
    def lrem(self, name, value):
        return self.connection.lrem(name, 0, value)

    @handle_key
    def setnx(self, key, value):
        return self.connection.setnx(key, self.serialize(value))

    def pipeline(self, transaction=True, shard_hint=None):
        return self.connection.pipeline(transaction, shard_hint)

    @handle_key
    def expire_second(self, key, second):
        """
        设置过期时间(单位为天)
        """
        return self.connection.expire(key, second)

    @handle_key
    def has(self, key):
        return self.connection.exists(key)
