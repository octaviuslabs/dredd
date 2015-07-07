from mem_store.base import Base
from mem_store.recommendation.thread_recommendation import ThreadRecommendation
import logging

class EmailThread(Base):
    def __init__(self, id_, account_id):
        self.id_ = id_
        self.account_id = account_id
        self.storage_key = ":".join(["account", self.account_id, "email_thread",  self.id_])
        self.emails = list()
        self.log_ident = "".join(["EmailThread ", self.id_, " for account ", self.account_id])

    def push(self, email):
        try:
            self.emails.append(email)
            self.compute_score()
            self.store().zadd(self.storage_key, email.sent_at.to_f(), email.storage_key)
            self.logging.info("Pushed email " + email.id_ + " onto " + self.log_ident )
            return True
        except Exception as e:
            self.logging.exception(e)
            return False

    def recommend(self):
        try:
            # Insert the score if a score has been set
            recommendation = ThreadRecommendation(self.score, self.account_id, self.id_, "question")
            recommendation.pop()
            recommendation.save()
            self.logging.info("Recommended " + self.log_ident )
            return True
        except AttributeError as e:
            # If the score does not exist, do not edit the recommendation
            self.logging.info("Did not recommend " + self.log_ident )
            return False
        except Exception as e:
            self.logging.exception(e)
            return False

    def has_newer(self, sent_at):
        return bool(self.get_items_after(sent_at))

    def get_items_after(self, sent_at):
        return self.store().zrangebyscore(self.storage_key, '(' + str(sent_at), "+inf")


    def get_items_before(self, sent_at):
        return self.store().zrevrangebyscore(self.storage_key, sent_at, 0.0)

    def compute_score(self):
        email = self.emails[0]
        if self.has_newer(email.sent_at.to_f()):
            self.logging.info("Keeping old score for " + self.log_ident )
            return False
        else:
            self.score = email.score
            return True
