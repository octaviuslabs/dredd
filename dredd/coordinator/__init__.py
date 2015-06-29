import json
import urllib2
import re
import time
import logging
from q import Q
from config import Configuration
from mem_store.email_message import EmailMessage
from mem_store.init_status_item import InitStatusItem
import traceback
from s3_url import S3Url
from boto.s3.key import Key
from boto.s3.connection import S3Connection

class NoMessage(Exception):
    pass


class Coordinator(object):
    config = Configuration()
    logger = logging.getLogger('dredd')

    def __init__(self, q_name):
        self.q_name = q_name
        self.retries = 0

    def get_task(self):
        messages = self.q().fetch_messages()
        if len(messages) <= 0:
            self.logger.info("No messages found")
            raise NoMessage
        self.message = messages[0]
        self.task = self._fetch_task_data(self.message.parsed_message())
        return self.task

    def clean(self):
        self.logger.info("Cleaning Message")
        self.clean_internal_init_status()
        return self.q().q().delete_message(self.message)

    def clean_internal_init_status(self):
        init_status = InitStatusItem(
            self.task.account_id,
            self.message.parsed_message()['type'],
            self.task.id_)
        init_status.finish_item()


    def _fetch_task_data(self, message):
        location = message.get("email", {}).get("url", None)
        try:
            if location == None:
                return None
            self.logger.info("Getting task from: " + str(location))
            s3_url = S3Url(location)
            bucket = self.store().get_bucket(s3_url.bucket_name)
            key = Key(bucket)
            key.key = s3_url.object_path
            raw_data = key.get_contents_as_string()
            return self._serialize_task(message, raw_data)
        except Exception, err:
            messags = "There was an error pulling task data from " + str(location) + "\n" + str(err)
            self.logger.critical(messags)
            raise Exception(messags)

    def _serialize_task(self, message, raw_data):
        task_type = message["type"]
        if task_type == "email":
            email_data = message["email"]
            lts_data = json.loads(raw_data)
            email_data.update(lts_data["email"])
            message = EmailMessage(email_data)
            self.logger.info("Built " + message.log_ident)
            return message
        self.logger.warn(task_type + " is not currently supported")
        return None

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = Q({q_name: self.q_name})
            return self.q_

    def store(self):
        try:
            return self.store_
        except:
            self.store_ = S3Connection(self.config.aws_access_key, self.config.aws_secret_access_key)
            return self.store_
