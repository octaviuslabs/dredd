from mem_store.base import Base

class Contact(Base):
    def __init__(self, id_):
        self.storage_key = ":".join(["contacts",  id_])
        self.id_ = id_