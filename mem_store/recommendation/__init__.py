import json
from mem_store.base import Base
import logging

class Recommendation(Base):
    def __init__(self, score, account_id):
        self.score = score
        self.account_id = account_id
        self.storage_key = ":".join(["recommendations",  account_id])

    def save(self):
        try:
            res = self.store().zadd(self.storage_key, self.score, self.to_json())
            logging.info("Adding recommendation " + str(self.to_dict()))
            return True
        except Exception as e:
            logging.critical(e)
            return False

    def to_dict(self):
        raise Exception("No to_dict defined")

    def to_json(self):
        return json.dumps(self.to_dict())
