import time

class VesperTime(object):
    # Expects time formatted like: "2015-02-23T21:22:48.000Z"
    def __init__(self, time_string):
        if not time_string:
            raise Exception("No time string specified in format '2015-02-23T21:22:48.000Z'")
        self.raw = time_string
        self.time_struct = self._read_from_string(time_string)

    def to_f(self):
        return time.mktime(self.time_struct)

    def to_s(self):
        return self.raw

    def _read_from_string(self, time_string):
        return time.strptime(time_string, "%Y-%m-%dT%H:%M:%S.%fZ")
