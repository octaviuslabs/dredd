from mem_store.base import Base as MemStoreBase
from lts_store import Base as LtsStoreBase
from model import ModelBase
import logging

class MemLtsStore(ModelBase, LtsStoreBase, MemStoreBase):
    logging = logging.getLogger('dredd')
