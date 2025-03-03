# -*- coding: utf-8 -*-
# from functools import wraps
# import json
import peewee
from .redis import BaseCache
from config import get_config


# Cacheable:用来定义缓存的
# CacheEvict:用来清理缓存
# CachePut:用来更新缓存
# @Caching

# 如果有缓存则返回缓存的，如果没有，则执行之后进行缓存
# 以key 传值 key=value
# index 传需要缓存的参数下标
def cache_able(prefix, key=None, index=None, expire=get_config().get("default_cache_expire_seconds")):
    def wrapper(func):
        def inner(*args, **kwargs):
            redis_cache = BaseCache()
            cache_key = handle_cache_key(prefix, key, index, *args, **kwargs)
            cache_value = redis_cache.get(cache_key)
            if cache_value:
                return cache_value
            cache_value = func(*args, **kwargs)
            if cache_value:  # 防止未查到数据也保存到缓存中了
                if isinstance(cache_value, peewee.ModelSelect):  # 数组与单个对象分开保存
                    redis_cache.set(cache_key, list(cache_value))
                else:
                    redis_cache.set(cache_key, cache_value)
                redis_cache.expire(cache_key, expire)
            return cache_value

        return inner

    return wrapper


# 删除缓存
def cache_evict(prefix, key=None, index=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            return_value = func(*args, **kwargs)
            redis_cache = BaseCache()
            cache_key = handle_cache_key(prefix, key, index, *args, **kwargs)
            redis_cache.delete(cache_key)
            return return_value

        return inner

    return wrapper


# 删除指定前缀的所有缓存
def cache_all_evict(prefix):
    def wrapper(func):
        def inner(*args, **kwargs):
            return_value = func(*args, **kwargs)
            redis_cache = BaseCache()
            redis_cache.clear(prefix + '*')
            return return_value

        return inner

    return wrapper


def handle_cache_key(prefix, key, index, *args, **kwargs):
    cache_key = prefix
    args_cache_key = ''
    if key is not None:
        value = kwargs.get(key)
        if value:
            args_cache_key = value
    if index and len(index) > 0:
        for i in index:
            if i == 0 and not args_cache_key:
                args_cache_key += str(args[i])
            else:
                args_cache_key += (":" + str(args[i]))
        cache_key = prefix + args_cache_key
    return cache_key


def push_cache(prefix, key=None, index=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            redis_cache = BaseCache()
            cache_key = handle_cache_key(prefix, key, index, *args, **kwargs)
            cache_value = func(*args, **kwargs)
            if cache_value:
                if isinstance(cache_value, peewee.Model):  # 数组与单个对象分开保存
                    redis_cache.push(cache_key, cache_value.id, True)
                else:
                    redis_cache.push(cache_key, cache_value, True)
            return cache_value

        return inner

    return wrapper
