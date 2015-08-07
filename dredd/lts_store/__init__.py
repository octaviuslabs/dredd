import redis
import json
import logging
from config import Configuration
from s3_url import S3Url
from boto.s3.key import Key
from boto.s3.connection import S3Connection

configuration = Configuration()

s3_store = S3Connection(
    configuration.aws_access_key,
    configuration.aws_secret_access_key)

class Base:
    def lts_store(self):
        try:
            return self.lts_store_
        except:
            self.lts_store_ = s3_store
            return self.lts_store_

    def lts_load(self, property_name):
        return self.lts_data_hash().get(property_name, None)

    def lts_data_hash(self):
        try:
            return self.lts_data_hash_
        except:
            self.lts_data_hash_ = json.loads(self.lts_data())
            return self.lts_data_hash_

    def get_url(self):
        try:
            return self.url
        except:
            raise "Object from LTS Store Base requires a `url` property or overloaded get_url()"

    def lts_data(self):
        try:
            return self.lts_data_
        except:
            self.lts_data_ = self.lts_fetch(self.get_url())
            return self.lts_data_

    def lts_fetch(self, url):
        s3_url = S3Url(url)
        bucket = self.lts_store().get_bucket(s3_url.bucket_name)
        key = Key(bucket)
        key.key = s3_url.object_path
        return key.get_contents_as_string()
