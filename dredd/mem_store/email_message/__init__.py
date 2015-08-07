import json
from dredd_time import DreddTime
from model.email_message import EmailMessage as EmailMessageModel
from mem_store.base import Base as MemStoreBase
from mem_store.email_thread import EmailThread
from model.contact import Contact
from text_set.message_body import MessageBody

class EmailMessage(EmailMessageModel, MemStoreBase):
    DEFAULT_EMAIL_THREAD_ID='threadless'

    @classmethod
    def load(klass, key):
        # WARNING: THIS IS HACKY BUT IT'S THE ONLY WAY WE CAN READ FROM THE STORE
        dummy_email_message = MemStoreBase()
        previous_email_json = dummy_email_message.store().get(key)

        # TODO: Figure out how to access the class object from a static method
        return klass(json.loads(previous_email_json))

    def types(self):
        return {
            'EmailThread': EmailThread,
            'Contact': Contact }

    def __init__(self, attrs):
        try:
            super(EmailMessage, self).__init__(attrs)
            self.committed = False
            self.storage_key = ":".join(["account", self.account_id, "email",  self.id_])
        except Exception as e:
            self.logging.exception(e)
            return None

    def _valid_body(self, body):
        if body == False:
            return False
        return True

    def save(self):
        if not self.is_valid() or self.committed:
            #raise if score is a problem
            self.logging.warn(self.log_ident + " is not valid or committed")
            return False
        try:
            self.thread.push(self)

            # Recommend the thread only if the email's score was calculated
            if self.score_calculated == True:
                self.thread.recommend()
            self.store().getset(self.storage_key, self.to_json())
            self.logging.info("Saved " + self.log_ident)
            return True
        except Exception as e:
            self.logging.exception(e)
            return False

    def to_dict(self):
        super_hash = super(EmailMessage, self).to_dict()
        super_hash.update({ 'body': self.body.raw })
        return super_hash


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
            self.logging.exception(e)
            return False
