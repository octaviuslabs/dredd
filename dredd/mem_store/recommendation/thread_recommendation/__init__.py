import json
from mem_store.recommendation import Recommendation

class ThreadRecommendation(Recommendation):
    def __init__(self, score, account_id, thread_id):
        super(ThreadRecommendation, self).__init__(score,account_id)
        self.thread_id = thread_id
        self.storage_value = ":".join(["email_thread", self.thread_id])

    def to_dict(self):
        return {
            "type": "email_thread",
            "id": self.thread_id,
            "score": self.score
        }
