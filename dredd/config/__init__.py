import os

class Configuration:
    def __init__(self, attrs=dict()):
        self.mem_store_host = self._locate_value("MEM_STORE_HOST", attrs)
        self.mem_store_port = self._locate_value("MEM_STORE_PORT", attrs)
        self.mem_store_database = self._locate_value('MEM_STORE_DB', attrs)
        self.mem_store_type = self._locate_value('MEM_STORE_TYPE', attrs)
        self.poll_interval = float(self._locate_value('POLL_INTERVAL', attrs))

        self.aws_access_key = self._locate_value('AWS_ACCESS_KEY_ID', attrs)
        self.aws_secret_access_key = self._locate_value('AWS_SECRET_ACCESS_KEY', attrs)
        self.q_region = self._locate_value('AWS_Q_REGION', attrs)
        self.poll_interval = float(self._locate_value('POLL_INTERVAL', attrs))
        self.aws_s3_bucket_name = self._locate_value("AWS_S3_BUCKET_NAME", attrs)
        self.pub_sub_prefix = self._locate_value('PUB_SUB_PREFIX', attrs)
        self.pub_sub_topic = self._locate_value('PUB_SUB_TOPIC', attrs)

    def _locate_value(self, key, attrs):
        try:
            return os.environ[key]
        except:
            self._fire_error(key + " not configured in environment")

    def _fire_error(self, message):
        raise Exception(message)
