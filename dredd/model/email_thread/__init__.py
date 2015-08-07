from model import ModelBase

class EmailThread(ModelBase):
    def __init__(self, id_, account_id):
        self.id_ = id_
        self.account_id = account_id
        self.emails = list()

    def compute_score(self):
        email = self.emails[0]
        if self.has_newer(email.sent_at.to_f()):
            self.logging.info("Keeping old score for " + self.log_ident )
            return False
        else:
            self.score = email.score
            return True

    def has_newer(self, sent_at):
        raise "Must override has_newer"
