import json
from dredd_time import DreddTime
from mem_store.base import Base
from mem_store.email_thread import EmailThread
from mem_store.contact import Contact
from mem_store.recommendation import Recommendation
from text_set.message_body import MessageBody



class EmailMessage(Base):
    DEFAULT_EMAIL_THREAD_ID='threadless'

    @classmethod
    def load(klass, key):
        # WARNING: THIS IS HACKY BUT IT'S THE ONLY WAY WE CAN READ FROM THE STORE
        dummy_email_message = Base()
        previous_email_json = dummy_email_message.store().get(key)

        # TODO: Figure out how to access the class object from a static method
        return klass(json.loads(previous_email_json))

    def __init__(self, attrs):
        try:
            self.id_ = attrs.get("id", "")
            if attrs.get("sent_at", False):
                self.sent_at = DreddTime(attrs.get("sent_at"))
            self.url = attrs.get("url")
            self.account_id = attrs.get("account_id")
            if attrs.get("account_contact_id", False):
                self.account_contact = Contact(attrs.get("account_contact_id"))
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
            self.storage_key = ":".join(["account", self.account_id, "email",  self.id_])
            self.log_ident = "".join(["Email ", self.id_, " for account ", self.account_id])
        except Exception as e:
            self.logging.critical(e)
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
        self.logging.info("Scoring " + self.log_ident)
        if self.features['question_count'] > 0:
            self.increase_score(1)
        if self.from_.id_ == self.account_contact.id_:
            self.increase_score()

        self.score_calculated = True
        return self.score

    def increase_score(self, amount=1):
        self.score += amount
        return self.score

    def save(self):
        if not self.is_valid() or self.committed:
            #raise if score is a problem
            self.logging.warn(self.log_ident + " is not valid or committed")
            return False
        try:
            self.thread.push(self)
            self.thread.recommend()
            self.store().getset(self.storage_key, self.to_json())
            self.logging.info("Saved " + self.log_ident)
            return True
        except Exception as e:
            self.logging.critical(e)
            return False

    def to_dict(self):
        to = list()
        for contact in self.to:
            to.append(contact)
        return {
            "id": self.id_,
            "account_id": self.account_id,
            "account_contact_id": self.account_contact.id_,
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
            self.account_contact.id_
            self.thread.id_
            self.sent_at.to_s()
            self.url
            self.from_.id_
            self.to
            self.subject
            self.body
            return True
        except AttributeError as e:
            self.logging.critical(e)
            return False
