import difflib
from model.email_message import EmailMessage
from text_set.message_body import MessageBody

class EmailMessageWithDiff(EmailMessage):

    def diff_with_message(self, previous_email):
        if previous_email == None:
            return

        distilled_body = self.distill_bodies(self.body, previous_email.body)
        self.processed_text = distilled_body

    def diff_with_previously_stored_message(self):
        self.diff_with_message(self.fetch_previous_message())

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


    def fetch_previous_message(self):
        raise "Must override fetch_previous_message"
