import json
from mem_store.base import Base

class Recommendation(Base):
    def __init__(self, score, account_id):
        self.score = float(score)
        self.account_id = account_id
        self.storage_key = ":".join(["recommendations",  account_id])
        self.log_ident = "".join(["Recommendation for account ", str(self.account_id), " of score " + str(self.score)])

    def save(self):
        try:
            self.store().zadd(self.storage_key, self.score, self.storage_value)
            self.logging.info("Added " + self.log_ident)
            return True
        except Exception as e:
            self.logging.critical(e)
            return False

    def pop(self):
        try:
            self.store().zrem(self.storage_key, self.storage_value)
            self.logging.info("Removed " + self.log_ident)
            return True
        except Exception as e:
            self.logging.critical(e)
            return False

    def value(self):
        raise Exception("No value defined")

    def to_dict(self):
        raise Exception("No to_dict defined")

    def to_json(self):
        return json.dumps(self.to_dict())
