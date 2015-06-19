from mem_store.base import Base
import logging
import time

class InitStatus(Base):
    logging = logging.getLogger('dredd')
    started_key = "init_status:started"


    def should_init(self):
        return bool(self.store().setnx(self.started_key, time.time()))

    def set_finished(self):
        return self.store().set("init_status:completed", time.time())

    # Use this method to signal a premature termination of the init process
    #   so later processes can pick up where this init left off
    def delete_init(self):
        return self.store().delete(self.started_key)
