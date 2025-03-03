try:
    from greenlet import getcurrent as get_ident
except Exception:
    from threading import get_ident


class Local(object):

    def __init__(self):
        self.storage = {}

    def __setitem__(self, k, v):
        ident = get_ident()
        if ident in self.storage:
            self.storage[ident][k] = v
        else:
            self.storage[ident] = {k: v}

    def __getitem__(self, k):
        ident = get_ident()
        if ident not in self.storage:
            self.storage[ident] = dict()
        return self.storage[ident].get(k, {})

    def __contains__(self, item):
        ident = get_ident()
        if ident not in self.storage:
            return False
        return item in self.storage[ident]

    def get(self, item, default=None):
        ident = get_ident()
        if ident not in self.storage:
            return default
        return self.storage[ident].get(item, default)

    def update(self, data):
        ident = get_ident()
        if ident not in self.storage:
            self.storage[ident] = dict()
        self.storage[ident].update(data)

    def to_dict(self):
        ident = get_ident()
        if ident not in self.storage:
            self.storage[ident] = dict()
        return self.storage[ident]

    def clear(self):
        ident = get_ident()
        self.storage[ident] = {}
