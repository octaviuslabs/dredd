import json 
from mem_store.email_thread import EmailThread
from model.contact import Contact
from model.email_message import EmailMessage as EmailMessageModel
from mem_lts_store import MemLtsStore
from text_set.message_body import MessageBody

class EmailMessage(EmailMessageModel, MemLtsStore):
    @classmethod
    def load(klass, key):
        # WARNING: THIS IS HACKY BUT IT'S THE ONLY WAY WE CAN READ FROM THE STORE
        dummy_email_message = MemLtsStore()
        previous_email_json = dummy_email_message.store().get(key)

        # TODO: Figure out how to access the class object from a static method
        return klass(json.loads(previous_email_json))

    def types(self):
        return {
        'EmailThread': EmailThread,
        'Contact': Contact }

    def __init__(self, attrs):
        super(EmailMessage, self).__init__(attrs)
        self.committed = False
        self.storage_key = ":".join(["account", self.account_id, "email",  self.id_])

    def get_body(self, attrs):
        body = self.lts_data_hash().get("email", {}).get("body", None)

        if body or body == "":
            return MessageBody(body)
        return None


    # Taken from mem_store.email_message
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
