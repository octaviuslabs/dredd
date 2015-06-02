import json
from vesper_time import VesperTime
from mem_store.base import Base
from mem_store.email_thread import EmailThread
from mem_store.contact import Contact
from mem_store.recommendation import Recommendation
from text_set.message_body import MessageBody

class EmailMessage(Base):
    DEFAULT_EMAIL_THREAD_ID='threadless'

    def __init__(self, attrs):
        self.id_ = attrs.get("id", "")
        if attrs.get("sent_at", None):
            self.sent_at = VesperTime(attrs.get("sent_at"))
        self.url = attrs.get("url")
        self.account_id = attrs.get("account_id")
        if attrs.get("thread_id", None):
            self.thread = EmailThread(attrs.get("thread_id"), self.account_id)
        self.raw_body = attrs.get("body")
        if attrs.get("from_id", None):
            self.from_ = Contact(attrs.get("from_id"))
        if attrs.get("to_ids", None):
            self.to = [Contact(i) for i in attrs.get("to_ids")]
        if attrs.get("cc_ids", None):
            self.cc = [Contact(i) for i in attrs.get("cc_ids")]
        if attrs.get("bcc_ids", None):
            self.bcc = [Contact(i) for i in attrs.get("bcc_ids")]
        self.subject = attrs.get("subject")
        if attrs.get("body", None):
            self.body = MessageBody(attrs.get("body"))
        self.processed_text = self.body
        self.features = {}
        self.score = float(0)
        self.score_calculated = False
        self.committed = False
        self.storage_key = ":".join(["emails",  self.id_])

    def add_feature(self, key, value):
        # It would be cooler if I could pass the classifier in here like ruby's rack
        self.features[key] = value
        return self.features

    def calculate_score(self):
        if self.features['question_count'] > 0:
            self.increase_score(1)
        self.score_calculated = True
        return self.score

    def increase_score(self, amount=1):
        self.score += amount
        return self.score

    def save(self):
        if self.is_valid() or self.committed:
            #raise if score is a problem
            return self
        # Store the recommendation
        recommendation = Recommendation(self.account_id)
        recommendation_listing = {
            "type": "email_thread",
            "id": self.thread.id_,
            "score": self.score
        }
        recommendation.push(self.score, recommendation_listing)
        # Push the email onto its thread
        self.thread.push(self)
        # Store the email its self
        self.store().getset(self.storage_key, self.to_json())
        return True
        # Error state???

    def _recommendation_listing(self):
        value = {
            "type": "email_thread",
            "id": self.thread.id_,
            "score": self.score
        }
        output = {
            "score": self.score,
            "value": value
        }
        return output

    def to_dict(self):
        to = list()
        for contact in self.to:
            to.append(contact)
        return {
            "id": self.id_,
            "account_id": self.account_id,
            "thread_id": self.thread.id_,
            "sent_at": self.sent_at.to_s(),
            "url": self.url,
            "from_id": self.from_.id_,
            "to_ids": [ contact.id_ for contact in self.to ],
            "cc_ids": [ contact.id_ for contact in self.cc ] ,
            "bcc_ids": [ contact.id_ for contact in self.bcc ],
            "subject": self.subject,
            "body": self.body.raw
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def is_valid(self):
        try:
            self.id_
            self.account_id
            self.thread.id_
            self.sent_at.to_s()
            self.url
            self.from_.id_
            self.to
            self.subject
            self.body
            return True
        except AttributeError:
            return False
