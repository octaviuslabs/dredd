from mem_store.base import Base

class EmailThread(Base):
    def __init__(self, id_, account_id):
        self.id_ = id_
        self.account_id = account_id
        self.storage_key = ":".join(["email_threads",  account_id, id_])

    def push(self, email):
        return self.store().zadd(self.storage_key, email.sent_at.to_f(), email.id_)
