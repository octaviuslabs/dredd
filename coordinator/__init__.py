import json
import urllib2
import re
import time
import logging
from q import Q
from config import Configuration
from mem_store.email_message import EmailMessage
import traceback
from s3_url import S3Url
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class Coordinator(object):
    config = Configuration()

    def __init__(self, q_name):
        self.q_name = q_name
        self.retries = 0

    def get_task(self):
        messages = self.q().fetch_messages()
        if len(messages) <= 0:
            logging.info("No messages found")
            return None
        self.message = messages[0]
        self.task = self._fetch_task_data(self.message.parsed_message())
        return self.task

    def clean(self):
        logging.info("Cleaning Message")
        return self.q().q().delete_message(self.message)

    def _fetch_task_data(self, message):
        location = message.get("email", {}).get("url", None)
        try:
            if location == None:
                return None
            logging.info("Getting task from: " + str(location))
            s3_url = S3Url(location)
            bucket = self.store().get_bucket(s3_url.bucket_name)
            key = Key(bucket)
            key.key = s3_url.object_path
            raw_data = key.get_contents_as_string()
            return self._serialize_task(message, raw_data)
        except Exception, err:
            messags = "There was an error pulling task data from " + str(location) + "\n" + str(err)
            logging.critical(messags)
            raise Exception(messags)

    def _serialize_task(self, message, raw_data):
        task_type = message["type"]
        if task_type == "email":
            email_data = message["email"]
            lts_data = json.loads(raw_data)
            email_data.update(lts_data["email"])
            message = EmailMessage(email_data)
            logging.info("Built " + message.log_ident)
            return message
        logging.warn(task_type + " is not currently supported")
        return None

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = Q(self.q_name)
            return self.q_

    def store(self):
        try:
            return self.store_
        except:
            self.store_ = S3Connection(self.config.aws_access_key, self.config.aws_secret_access_key)
            return self.store_
