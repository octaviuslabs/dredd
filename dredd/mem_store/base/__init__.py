import redis
import json
import logging
from config import Configuration
mem_store_config = Configuration()
store = redis.StrictRedis(host=mem_store_config.mem_store_host, port=mem_store_config.mem_store_port, db=mem_store_config.mem_store_database)

class Base(object):
    logging = logging.getLogger('dredd')
    def __init__(self):
        return

    def store(self):
        try:
            return self._store
        except AttributeError:
            self._store = store
            return self._store
