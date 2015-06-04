import os

class Configuration:
    def __init__(self, attrs=dict()):
        self.mem_store_host = self._locate_value("MEM_STORE_HOST", attrs)
        self.mem_store_port = self._locate_value("MEM_STORE_PORT", attrs)
        self.mem_store_database = self._locate_value('MEM_STORE_DB', attrs)
        self.mem_store_type = self._locate_value('MEM_STORE_TYPE', attrs)
        self.poll_interval = float(self._locate_value('POLL_INTERVAL', attrs))
        self.queue_endpoint = self._locate_value('QUEUE_ENDPOINT', attrs)

        self.aws_access_key = self._locate_value('AWS_ACCESS_KEY_ID', attrs)
        self.aws_secret_access_key = self._locate_value('AWS_SECRET_ACCESS_KEY', attrs)


        #self._locate_value('AWS_SECRET_ACCESS_KEY', attrs) #Move to env var
        self.q_name = "dev_dredd-dev_message_bodies" #"dev_dredd-dev_message_bodies"
        self.q_region = "us-east-1"


    def _locate_value(self, key, attrs):
        try:
            return os.environ[key]
        except:
            self._fire_error(key + " not configured in environment")

    def _fire_error(self, message):
        raise Exception(message)
