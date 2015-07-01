from q import Q

class SqSManager(object):
    def __init__(self, q_name):
        self.q_name = q_name
        self.retries = 0

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = Q(self.q_name)
            return self.q_

    def clean(self, message):
        self.logger.info("Cleaning Message")
        return self.q().delete_message(message)
