from mem_store.base import Base
import logging

class InitStatusItem(Base):
    logging = logging.getLogger('dredd')
    def __init__(self, account_id, type_, id_):
        self.storage_key_root = ":".join(["init_status", "accounts", account_id, type_])
        self.id_ = id_

    def status(self):
        if self.sismember(self.get_pending_item_storage_key(), self.id_) == 1:
            return "pending"
        elif self.sismember(self.get_finished_item_storage_key(), self.id_) == 1:
            return "finished"
        else:
            return "unknown"


    def add_item(self):
        return self.sadd(self.get_pending_item_storage_key(), self.id_)

    def finish_item(self):
        result = self.store().srem(self.get_pending_item_storage_key(), self.id_)
        if result != 0:
            self.sadd(self.get_finished_item_storage_key(), self.id_)

    def sadd(self, key, id):
        self.store().sadd(key, id)

    def sismember(self, key, id):
        self.store().sismember(key, id)


    def get_pending_item_storage_key(self):
        return ":".join([self.storage_key_root, "pending"])

    def get_finished_item_storage_key(self):
        return ":".join([self.storage_key_root, "finished"])
