from event_scorer import EventScorer
from mem_store.recommendation.thread_recommendation import ThreadRecommendation

class EmailMessageSimplePropertyScorer(EventScorer):
    def __init__(self, email_message):
        self.event_email_message = email_message

    def save(self):
        # Set up indexes
        if self.is_last_message_in_thread():
            self.judge_self_sender()
            self.judge_last_sent()

        # Persist the object
        # (warning: this step gets repeated across each Dredd daemon, it is redundant)
        return self.event_email_message.save()


    def is_last_message_in_thread(self):
        if self.event_email_message.thread.has_newer(self.sent_at_to_f()):
            return False
        else:
            return True

    def judge_self_sender(self):
        score = self.self_sender_value()
        recommendation = ThreadRecommendation(
            score,
            self.event_email_message.account_id,
            self.event_email_message.thread.id_,
            "self_sender")
        recommendation.save()

    def self_sender_value(self):
        if self.event_email_message.account_contact.id_ == self.event_email_message.from_.id_:
            return 1.0
        else:
            return 0.0

    def judge_last_sent(self):
        score = self.sent_at_to_f()
        recommendation = ThreadRecommendation(
            score,
            self.event_email_message.account_id,
            self.event_email_message.thread.id_, 
            "last_sent")
        recommendation.save()


    def sent_at_to_f(self):
        return self.event_email_message.sent_at.to_f()
