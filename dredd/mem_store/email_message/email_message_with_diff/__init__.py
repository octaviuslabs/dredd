import json
import difflib
from mem_store.email_message import EmailMessage
from text_set.message_body import MessageBody

from IPython import embed

class EmailMessageWithDiff(EmailMessage):
    def __init__(self, attrs):
        # Initialize
        super(EmailMessageWithDiff, self).__init__(attrs)

        # Fetch old body from store
        distilled_body = self.body
        previous_bodies = self.thread.get_items_before(self.sent_at.to_f())
        if len(previous_bodies) > 0:
            previous_email_json = self.store().get(previous_bodies[0])
            previous_email = EmailMessage(json.loads(previous_email_json))
            distilled_body = self.distill_bodies(self.body, previous_email.body)

        # Set self.processed_text to the diffs you just done did
        self.processed_text = distilled_body



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