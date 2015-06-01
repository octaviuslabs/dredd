import redis
import json
store = redis.StrictRedis(host='localhost', port=6379, db=0)

class Base(object):
    def __init__(self):
        return

    def store(self):
        try:
            return self._store
        except AttributeError:
            self._store = store
            return self._store
