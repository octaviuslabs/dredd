from mem_store.base import Base
import logging

class InitStatusItem(Base):
    logging = logging.getLogger('dredd')
    def __init__(self, account_id, type_, id_):
        self.storage_key_root = ":".join(["init_status", "accounts", account_id, type_])
        self.id_ = id_

    def status(self):
        if self.store().sismember(self.get_pending_item_storage_key(), self.id_) == 1:
            return "pending"
        elif self.store().sismember(self.get_finished_item_storage_key(), self.id_) == 1:
            return "finished"
        else:
            return "unknown"


    def add_item(self):
        return self.store().sadd(self.get_pending_item_storage_key(), self.id_)

    def finish_item(self, type_, id_):
        pending_item_storage_key = self.get_pending_item_storage_key()
        result = self.store.srem(pending_item_storage_key, id_)
        if result != 0:
            self.store.sadd(self.get_finished_item_storage_key(), id_)


    def get_pending_item_storage_key(self):
        return ":".join([self.storage_key_root, "pending"])

    def get_finished_item_storage_key(self):
        return ":".join([self.storage_key_root, "finished"])
