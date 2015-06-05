from mem_store.base import Base
from mem_store.recommendation.thread_recommendation import ThreadRecommendation
import logging

class EmailThread(Base):
    def __init__(self, id_, account_id):
        self.id_ = id_
        self.account_id = account_id
        self.storage_key = ":".join(["email_threads",  account_id, id_])
        self.score = float(0)
        self.emails = list()

    def push(self, email):
        try:
            self.emails.append(email)
            self.compute_score()
            self.store().zadd(self.storage_key, email.sent_at.to_f(), email.id_)
            logging.info("Pushed " + email.id_ + " onto email thread " + str(self.id_) )
            return True
        except Exception as e:
            logging.critical(e)
            return False

    def save(self, email):
        try:
            recommendation = ThreadRecommendation(self.score, self.account_id, self.id_)
            recommendation.save()
            return True
        except Exception as e:
            logging.critical(e)
            return False

    def compute_score(self):
        self.score = self.emails[0].score # to be replaced with better scoring logic
        return self.score
