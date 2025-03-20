from functools import wraps

from .redis import BaseCache
from .exception import CacheKeyError, CacheSetError, CacheValueError  # noqa

Cache = BaseCache


def using_cache(namespace=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if namespace is not None:
                try:
                    # Convention: module name with the first letter capitalized + "Cache"
                    cache = globals()[f'{namespace.lower().capitalize()}Cache'](namespace)
                except KeyError:
                    cache = BaseCache(namespace)
            else:
                raise RuntimeError('Missing namespace.')
            kwargs['cache'] = cache
            return func(*args, **kwargs)

        return wrapper

    return decorator
