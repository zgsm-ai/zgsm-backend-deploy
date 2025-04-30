# -*- coding: utf-8 -*-
# from functools import wraps
# import json
import peewee
from .redis import BaseCache
from config import get_config


# Cacheable: used to define cache
# CacheEvict: used to clear cache
# CachePut: used to update cache
# @Caching

# If there is a cache, return the cached value; if not, execute and then cache
# Pass the value with key=value
# Index passes the parameter index to be cached
def cache_able(prefix, key=None, index=None, expire=get_config().get("default_cache_expire_seconds")):
    def wrapper(func):
        def inner(*args, **kwargs):
            redis_cache = BaseCache()
            cache_key = handle_cache_key(prefix, key, index, *args, **kwargs)
            cache_value = redis_cache.get(cache_key)
            if cache_value:
                return cache_value
            cache_value = func(*args, **kwargs)
            if cache_value:  # Prevent saving to cache when no data is found
                if isinstance(cache_value, peewee.ModelSelect):  # Store arrays and single objects separately
                    redis_cache.set(cache_key, list(cache_value))
                else:
                    redis_cache.set(cache_key, cache_value)
                redis_cache.expire(cache_key, expire)
            return cache_value

        return inner

    return wrapper


# Delete cache
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


# Delete all cache with the specified prefix
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
                if isinstance(cache_value, peewee.Model):  # Store arrays and single objects separately
                    redis_cache.push(cache_key, cache_value.id, True)
                else:
                    redis_cache.push(cache_key, cache_value, True)
            return cache_value

        return inner

    return wrapper
