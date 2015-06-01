import json
from mem_store.base import Base

class Recommendation(Base):
    def __init__(self, account_id):
        self.account_id = account_id
        self.storage_key = ":".join(["recommendations",  account_id])

    def push(self, score, item):
        return self.store().zadd(self.storage_key, score, json.dumps(item))
