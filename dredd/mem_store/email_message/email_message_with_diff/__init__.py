import json
import difflib
from mem_store.email_message import EmailMessage
from text_set.message_body import MessageBody
from mem_store.base import Base

class EmailMessageWithDiff(EmailMessage):

    @classmethod
    def load(klass, key):
        # WARNING: THIS IS HACKY BUT IT'S THE ONLY WAY WE CAN READ FROM THE STORE
        dummy_email_message = Base()
        previous_email_json = dummy_email_message.store().get(key)

        # TODO: Figure out how to access the class object from a static method
        return klass(json.loads(previous_email_json))

    def __init__(self, attrs):
        # Initialize
        super(EmailMessageWithDiff, self).__init__(attrs)

    def diff_with_message(self, previous_email):
        if previous_email == None:
            return

        distilled_body = self.distill_bodies(self.body, previous_email.body)
        self.processed_text = distilled_body

    def diff_with_previously_stored_message(self):
        self.diff_with_message(self.fetch_previous_message())

    def fetch_previous_message(self):
        old_body_keys = self.thread.get_items_before(self.sent_at.to_f())
        if len(old_body_keys) > 0:
            return self.get_message(old_body_keys[0])
        else:
            return None

    def get_message(self, key):
        previous_email_json = self.store().get(key)
        return EmailMessage(json.loads(previous_email_json))

    def distill_bodies(self, body, previous_body):
        new_sentences = [item.sentence for item in body.sentences()]
        old_sentences = [item.sentence for item in previous_body.sentences()]
        return MessageBody(" ".join(self.new_content(new_sentences, old_sentences)))

    def new_content(self, new, old):
        # Returns a list of sentences which are new to a message body compared
        #   to an older message body
        diffs = difflib.ndiff(old, new)
        diff_list = list(diffs)
        return [sentence[2:] for sentence in diff_list if sentence.startswith('+ ')]
