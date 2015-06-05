from mem_store.base import Base
from mem_store.recommendation.thread_recommendation import ThreadRecommendation
import logging

class EmailThread(Base):
    def __init__(self, id_, account_id):
        self.id_ = id_
        self.account_id = account_id
        self.storage_key = ":".join(["email_threads",  account_id, id_])
        self.emails = list()
        self.log_ident = "".join(["EmailThread ", self.id_, " for account ", self.account_id])

    def push(self, email):
        try:
            self.emails.append(email)
            self.compute_score()
            self.store().zadd(self.storage_key, email.sent_at.to_f(), email.id_)
            self.logging.info("Pushed email " + email.id_ + " onto " + self.log_ident )
            return True
        except Exception as e:
            self.logging.critical(e)
            return False

    def recommend(self):
        try:
            recommendation = ThreadRecommendation(self.score, self.account_id, self.id_)
            recommendation.pop()
            recommendation.save()
            self.logging.info("Recommended " + self.log_ident )
            return True
        except AttributeError as e:
            self.logging.info("Did not recommend " + self.log_ident )
            return False
        except Exception as e:
            self.logging.critical(e)
            return False

    def has_newer(self, sent_at):
        return bool(self.get_items_after(sent_at))

    def get_items_after(self, sent_at):
        return self.store().zrangebyscore(self.storage_key, sent_at, "+inf")

    def compute_score(self):
        email = self.emails[0] # In the future scoring can take in to account all of the emails
        if self.has_newer(email.sent_at.to_f()):
            self.logging.info("Keeing old score for " + self.log_ident )
            return False
        else:
            self.score = email.score
            return True
