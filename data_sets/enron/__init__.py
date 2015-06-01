from pymongo import MongoClient
from mem_store.email_message import EmailMessage

class EnronData:
    DEFAULT_SAMPLE_SIZE = 1000

    def pull_emails(self, sample_size=DEFAULT_SAMPLE_SIZE):
        client = MongoClient()
        db = client.enron_mail
        messages = db.messages
        emails = list()
        sample = messages.find_one()
        for message in messages.find():
            email = self._new_email_object(message)
            emails.append(email)
            if len(emails) >= sample_size:
                break
        return emails

    def _new_email_object(self, message):
        email_attrs = {
            "account_id": "enron_data_set",
            "subject": message.get('headers', {}).get('Subject', "No subject"),
            "from_id": message.get('headers', {}).get('From', "No From"),
            "to_ids": [message.get('headers', {}).get('To', "No To")],
            "body": message.get('body')
        }
        return EmailMessage(email_attrs)
