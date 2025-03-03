class CacheError(Exception):
    pass


class CacheNoConnectionError(CacheError):
    def __init__(self, err=('Create a connection pool before using cache. \n'
                            'eg. Cache.create_pool(url)')):
        super().__init__(err)


class CacheKeyError(KeyError):
    def __init__(self, err='缓存中未存有该键值'):
        super().__init__(err)


class CacheValueError(ValueError):
    def __init__(self, err=''):
        super().__init__(err)


class CacheSetError(RuntimeError):
    def __init__(self, err=''):
        super().__init__(err)
