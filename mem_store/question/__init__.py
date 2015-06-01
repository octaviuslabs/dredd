from mem_store.base import Base

class Question(Base):
    def __init__(self, email_id):
        self.storage_key = ":".join(["questions", email_id])

    def push(self, score, question_text):
        return self.store().zadd(self.storage_key, score, question_text)
