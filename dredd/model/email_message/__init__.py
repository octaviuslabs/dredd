import json
from model import ModelBase
from model.contact import Contact
from model.email_thread import EmailThread
from dredd_time import DreddTime
from text_set.message_body import MessageBody

class EmailMessage(ModelBase):
    def types(self):
        return {
            'EmailThread': EmailThread,
            'Contact': Contact }

    def __init__(self, attrs):
        try:
            self.id_ = attrs.get("id", "")
            if attrs.get("sent_at", False):
                self.sent_at = DreddTime(attrs.get("sent_at"))
            self.url = attrs.get("url")
            self.account_id = attrs.get("account_id")
            if attrs.get("account_contact_id", False):
                self.account_contact = self.get_type('Contact')(attrs.get("account_contact_id"))
            if attrs.get("thread_id", False):
                self.thread = self.get_type('EmailThread')(attrs.get("thread_id"), self.account_id)
            if attrs.get("from_id", False):
                self.from_ = self.get_type('Contact')(attrs.get("from_id"))
            self.to = [self.get_type('Contact')(i) for i in attrs.get("to_ids", list())]
            self.cc = [self.get_type('Contact')(i) for i in attrs.get("cc_ids", list())]
            self.bcc = [self.get_type('Contact')(i) for i in attrs.get("bcc_ids", list())]
            self.subject = attrs.get("subject")
            self.body = self.get_body(attrs)
            self.processed_text = self.body
            self.features = {}
            self.score = float(0)
            self.score_calculated = False
            self.log_ident = "".join(["Email ", self.id_, " for account ", self.account_id])
        except Exception as e:
            self.logging.exception(e)
            return None

    def get_type(self, type_name):
        return self.types()[type_name]

    def _valid_body(self, body):
        if body == False:
            return False
        return True

    def get_body(self, attrs):
        body = attrs.get("body", None)
        if body or body == "":
            return MessageBody(attrs.get("body"))
        return None

    def add_feature(self, key, value):
        # It would be cooler if I could pass the classifier in here like ruby's rack
        self.features[key] = value
        return self.features

    def calculate_score(self):
        self.logging.info("Scoring " + self.log_ident)
        if self.features['question_count'] > 0:
            self.increase_score(1)

        self.score_calculated = True
        return self.score

    def increase_score(self, amount=1):
        self.score += amount
        return self.score

    def to_json(self):
        return json.dumps(self.to_dict())

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
            "subject": self.subject
        }

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
            return True
        except AttributeError as e:
            self.logging.exception(e)
            return False
