from config import Configuration
from coordinator.q import Q
import logging
from mem_store.init_status_item import InitStatusItem
from boto.s3.connection import S3Connection
from coordinator.q.dredd_message.dredd_email_message import DreddEmailMessage
from IPython import embed
import json

class QPrimer(object):
    config = Configuration()
    logger = logging.getLogger('dredd')

    def __init__(self):
        self.q_name = self.config.q_name

    def prime(self):
        self.logger.info("Priming Dredd.")
        self.bucket_list()

    def bucket_list(self):
        bucket = self.store().get_bucket(self.config.aws_s3_bucket_name)

        accounts_list = [account_prefix.name for account_prefix in bucket.list('accounts/', '/')]
        for account_prefix in accounts_list:
            threads_list = [thread_prefix.name for thread_prefix in bucket.list(account_prefix + u'threads/', '/')]
            for thread_prefix in threads_list:
                email_list = [email_prefix.name for email_prefix in bucket.list(thread_prefix + u'emails/', '/')]
                for email_path in email_list:
                    self.logger.info("Found email %s" % email_path)
                    self.enqueue_email_path(email_path)


    def enqueue_email_path(self, email_path):
        parsed_path = self.parse_path(email_path)
        init_status_item = InitStatusItem(
            parsed_path["account_id"],
            "email",
            parsed_path["email_id"])

        # If the item is already queued or processed, don't re-queue it
        if init_status_item.status() in ["finished", "pending"]:
            return

        init_status_item.add_item()

        # Add item to queue
        queue_message = DreddEmailMessage(
            self.config.aws_s3_bucket_name,
            email_path)
        self.q().post_message(queue_message)

    def parse_path(self, path):
        split_path = path.split("/")

        return {
            "account_id": split_path[1],
            "thread_id": split_path[3],
            "email_id": split_path[5][:-5] # remove '.json' from the end of the string
        }

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = Q(self.q_name)
            # self.q_.set_message_class(DreddMessage)
            return self.q_


    def store(self):
        try:
            return self.store_
        except:
            self.store_ = S3Connection(self.config.aws_access_key, self.config.aws_secret_access_key)
            return self.store_
