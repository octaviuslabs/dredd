from event_scorer import EventScorer
from mem_store.email_message import EmailMessage
from mem_store.email_message.email_message_with_diff import EmailMessageWithDiff
import logging

class EmailMessageScorer(EventScorer):
    logging = logging.getLogger('dredd')

    def __init__(self, email_message, classifier):
        self.event_email_message = email_message
        self.classifier = classifier

        super(EmailMessageScorer, self).__init__()

    def save(self):
        later_items = self.get_later_items()

        later_items_length = len(later_items)
        if later_items_length == 0:
            # Calling event_email_message.save() at the end of this function
            #   propigates the score up to the thread
            self.event_email_message.score = self.score_message(self.event_email_message)

        elif later_items_length == 1:
            latest_message = self.get_latest_message_diff()
            self.event_email_message.thread.score = self.score_message(latest_message)

            # Override the thread's score explicitly because event_email_message.save()
            #   isn't responsible for this information
            self.event_email_message.thread.recommend()

        else:
            pass

        # Persist email itself in store
        return self.event_email_message.save()

    def get_later_items(self):
        return self.event_email_message.thread.get_items_after(
            self.event_email_message.sent_at.to_f())

    def get_latest_message_diff(self):
        later_items = self.get_later_items()
        latest_message = EmailMessageWithDiff.load(later_items[0])
        latest_message.diff_with_message(self.event_email_message)
        return latest_message

    def score_message(self, email_message):
        email_message.processed_text.classify_questions(self.classifier)
        email_message.add_feature('question_count', len(email_message.processed_text.questions))
        email_message.add_feature('non_question_count',  len(email_message.processed_text.non_questions))
        score = email_message.calculate_score()
        self.logging.info(str(score))
        return score
