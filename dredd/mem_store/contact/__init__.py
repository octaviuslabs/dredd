from mem_store.base import Base
import logging

class Contact(Base):
    logging = logging.getLogger('dredd')
    def __init__(self, id_):
        self.storage_key = ":".join(["contacts",  id_])
        self.id_ = id_
