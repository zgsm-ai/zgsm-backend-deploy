#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import functools
import time
import uuid
import redis

from lib.cache import Cache
from lib.cache.cache_anno import handle_cache_key

cache = Cache()


class BaseLock:

    def __init__(self, acquire_time):
        self.acquire_time = acquire_time
        self.key = None
        self.value = None

    def get_lock(self, *args, **kwargs):
        raise NotImplementedError

    def release_lock(self, *args, **kwargs):
        raise NotImplementedError


class RedisLock(BaseLock):
    """Redis lock, limit concurrent operations through Redis"""

    def get_lock(self, key, *args, **kwargs):
        """Get Redis lock"""
        self.key = key
        end = time.time() + self.acquire_time
        while time.time() < end:
            value = uuid.uuid1().hex
            if cache.setnx(self.key, value):
                self.value = value
                cache.expire_second(self.key, self.acquire_time)
                return True
            else:
                continue
        return False

    def release_lock(self, *args, **kwargs):
        """Release lock"""
        pip = cache.pipeline(True)
        while True:
            try:
                pip.watch(self.key)
                lock_value = cache.get(self.key)
                if not lock_value:
                    return True
                if lock_value == self.value:
                    # Delete cached key
                    pip.multi()
                    pip.delete(self.key)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except redis.exceptions.WatchError:
                pass
        return False

    def get_perform_lock(self, key):
        """Get execution lock"""
        value = uuid.uuid1().hex
        if cache.setnx(key, value):
            cache.expire_second(key, self.acquire_time)
            return True
        else:
            return False

    def clear_perform_lock(self, key):
        """Release execution lock"""
        cache.clear(key)


def lock_check(lock: BaseLock, key=None, prefix='lock_key', index=None):
    # Redis lock, limit concurrent operations
    def inner(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            new_key = key
            if index:
                new_key = handle_cache_key(prefix, key, index, *args, **kwargs)
            if lock.get_lock(new_key):
                res = func(*args, **kwargs)
                lock.release_lock()
                return res
            else:
                lock.release_lock()
                return func(*args, **kwargs)

        return wrap

    return inner


def perform_lock(prefix='perform_lock_key', key=None):
    def inner(func):
        @functools.wraps(func)
        def warp(*args, **kwargs):
            cache_key = handle_cache_key(prefix, key, None, *args, **kwargs)
            end = time.time() + 60
            while time.time() < end:
                if cache.get(cache_key):
                    time.sleep(1)
                else:
                    break
            return func(*args, **kwargs)

        return warp

    return inner
