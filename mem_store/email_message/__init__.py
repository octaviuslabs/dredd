import json
from vesper_time import VesperTime
from mem_store.base import Base
from mem_store.email_thread import EmailThread
from mem_store.contact import Contact
from mem_store.recommendation import Recommendation
from text_set.message_body import MessageBody
import logging



class EmailMessage(Base):
    DEFAULT_EMAIL_THREAD_ID='threadless'

    def __init__(self, attrs):
        try:
            self.id_ = attrs.get("id", "")
            if attrs.get("sent_at", False):
                self.sent_at = VesperTime(attrs.get("sent_at"))
            self.url = attrs.get("url")
            self.account_id = attrs.get("account_id")
            if attrs.get("thread_id", False):
                self.thread = EmailThread(attrs.get("thread_id"), self.account_id)
            if attrs.get("from_id", False):
                self.from_ = Contact(attrs.get("from_id"))
            self.to = [Contact(i) for i in attrs.get("to_ids", list())]
            self.cc = [Contact(i) for i in attrs.get("cc_ids", list())]
            self.bcc = [Contact(i) for i in attrs.get("bcc_ids", list())]
            self.subject = attrs.get("subject")
            body = attrs.get("body", None)
            if body or body == "":
                self.body = MessageBody(attrs.get("body"))
            self.processed_text = self.body
            self.features = {}
            self.score = float(0)
            self.score_calculated = False
            self.committed = False
            self.storage_key = ":".join(["emails",  self.id_])
            self.log_ident = "".join(["Email ", self.id_, " for account ", self.account_id])
        except Exception as e:
            logging.critical(e)
            return None

    def _valid_body(self, body):
        if body == False:
            return False
        return True


    def add_feature(self, key, value):
        # It would be cooler if I could pass the classifier in here like ruby's rack
        self.features[key] = value
        return self.features

    def calculate_score(self):
        logging.info("Scoring " + self.log_ident)
        if self.features['question_count'] > 0:
            self.increase_score(1)
        self.score_calculated = True
        return self.score

    def increase_score(self, amount=1):
        self.score += amount
        return self.score

    def save(self):
        if not self.is_valid() or self.committed:
            #raise if score is a problem
            logging.warn(self.log_ident + " is not valid or committed")
            return False
        # Store the recommendation
        try:
            self.push(email)
            self.thread.save()
            self.store().getset(self.storage_key, self.to_json())
            logging.warn("Saved " + self.log_ident)
            return True
        except Exception as e:
            logging.critical(e)
            return False

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
        except AttributeError as e:
            logging.critical(e)
            return False
