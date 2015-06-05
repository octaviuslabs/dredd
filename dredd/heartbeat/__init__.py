import time
import logging

class Heartbeat:
    logging = logging.getLogger('dredd')
    def __init__(self):
        self.last_heartbeat = None

    def send_heartbeat(self):
        current_time = self.current_time()
        if self.last_heartbeat is None:
            return self._deliver()

        if (current_time - self.last_heartbeat) > 30:
            return self._deliver()

        return self.last_heartbeat

    def _deliver(self):
        self.last_heartbeat = self.current_time()
        # self.logging.info("Sent Heartbeat")
        #Heartbeat_code_goes Here
        return self.last_heartbeat

    def current_time(self):
        return time.time()
