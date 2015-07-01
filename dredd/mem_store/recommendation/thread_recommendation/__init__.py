import json
from mem_store.recommendation import Recommendation

class ThreadRecommendation(Recommendation):
    @classmethod
    def get_recommendations(klass, account_id, score_type):
        # TODO: This is hacky, but only way to access store at this time
        klass_instance = klass(0.0, account_id, 'dummy_thread_id', score_type)
        return klass_instance.store().zrangebyscore(klass_instance.storage_key, '-inf', '+inf', withscores=True)

    def __init__(self, score, account_id, thread_id, score_type):
        super(ThreadRecommendation, self).__init__(score,account_id)
        self.thread_id = thread_id
        self.score_type = score_type
        self.storage_value = ":".join(["account", self.account_id, "email_thread", self.thread_id])
        self.storage_key = ":".join(["account", self.account_id, "judgement", "email_thread", self.score_type])

    def to_dict(self):
        return {
            "type": "email_thread",
            "id": self.thread_id,
            "score": self.score,
            "score_type": self.score_type
        }
