class SqSManager(object):
    def __init__(self, q_name):
        self.q_name = q_name
        self.retries = 0

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = Q({q_name: self.q_name})
            return self.q_
