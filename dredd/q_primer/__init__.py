from config import Configuration
from coordinator.q import Q
import logging
from mem_store.init_status_item import InitStatusItem
from boto.s3.connection import S3Connection
from coordinator.q.dredd_message.dredd_email_message import DreddEmailMessage
import json

class QPrimer(object):
    config = Configuration()
    logger = logging.getLogger('dredd')


    def __init__(self):
        self.q_name = self.config.q_name
        self.bucket = self.store().get_bucket(self.config.aws_s3_bucket_name)

    def prime(self):
        self.logger.info("Priming Dredd.")
        self.traverse_accounts_and_queue()

    # Traverse buckets depth-first by account
    def traverse_accounts_and_queue(self):
        accounts_list =  self.account_prefixes()
        for account_prefix in accounts_list:
            threads_list =  self.thread_prefixes_for_account(account_prefix)
            for thread_prefix in threads_list:
                email_list = self.email_items_for_thread_prefix(thread_prefix)
                for email_path in email_list:
                    self.logger.info("Found email %s" % email_path)
                    self.enqueue_email_path(email_path)

    # Returns a list of keys or prefixes from the QPrimer's bucket and a given
    #   prefix. (e.g. listing with a prefix of 'accounts/'
    #   returns ['accounts/a', 'accounts/b', ...])
    def bucket_list(self, prefix, delimeter="/"):
        return [item.name for item in self.bucket.list(prefix, delimeter)]

    def account_prefixes(self):
        return self.bucket_list('accounts/')

    def thread_prefixes_for_account(self, account_prefix):
        return self.bucket_list(account_prefix + 'threads/')

    def email_items_for_thread_prefix(self, thread_prefix):
        return self.bucket_list(thread_prefix + 'emails/')


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

    # Split an email path into the parts that make it up (i.e. account id,
    #   thread id, email id). Returns a hash.
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
            return self.q_


    def store(self):
        try:
            return self.store_
        except:
            self.store_ = S3Connection(self.config.aws_access_key, self.config.aws_secret_access_key)
            return self.store_
