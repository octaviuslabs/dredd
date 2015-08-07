from model import ModelBase
import logging

class Contact(ModelBase):
    logging = logging.getLogger('dredd')
    def __init__(self, id_):
        self.storage_key = ":".join(["contacts",  id_])
        self.id_ = id_
