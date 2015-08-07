import json
from model.email_message.email_message_with_diff import EmailMessageWithDiff as EmailMessageWithDiffModel
from mem_lts_store.email_message import EmailMessage

class EmailMessageWithDiff(EmailMessage, EmailMessageWithDiffModel):
    def __init__(self, attrs):
        super(EmailMessageWithDiff, self).__init__(attrs)

    def fetch_previous_message(self):
        old_body_keys = self.thread.get_items_before(self.sent_at.to_f())
        if len(old_body_keys) > 0:
            return self.get_message(old_body_keys[0])
        else:
            return None

    def get_message(self, key):
        previous_email_json = self.store().get(key)
        return EmailMessage(json.loads(previous_email_json))
