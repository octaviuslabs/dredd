import boto.sqs
import json
from config import Configuration
from coordinator.q.dredd_message import DreddMessage
import logging


class Q(object):
    config = Configuration()
    GET_VISIBILITY =60

    def __init__(self, queue_name):
        self.queue_name = queue_name

    def client(self):
        try:
            return self.client_
        except:
            self.client_ = boto.sqs.connect_to_region(
                    self.config.q_region,
                    aws_access_key_id=self.config.aws_access_key,
                    aws_secret_access_key=self.config.aws_secret_access_key)
            return self.client_

    def q(self):
        try:
            return self.q_
        except:
            self.q_ = self.client().get_queue(self.queue_name)
            self.q_.set_message_class(DreddMessage)
            return self.q_

    def fetch_messages(self):
        try:
            messages = self.q().get_messages()
            if len(messages) > 0:
                message_types = [ message.parsed_message().get("type", "no-type") for message in messages]
                logging.info("Got " +  ".".join(message_types) + " messages" )
            return messages
        except Exception as err:
            logging.critical(err)
            return list()

# {
#   "Type" : "Notification",
#   "MessageId" : "66ca8ffc-5c97-5852-b521-c2151aa3400d",
#   "TopicArn" : "arn:aws:sns:us-east-1:242236168477:dev_message_bodies",
#   "Message" : "{\"id\":\"dad085\",\"message\":{\"email\":{\"id\":\"ef45e5e2-ede2-483f-ab5c-ea453028ec64\",\"sent_at\":\"2015-05-12T17:51:35.000Z\",\"url\":\"https://vesper-lts-development.s3.amazonaws.com/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json\",\"deleted_at\":null,\"thread_id\":\"e767c1dc-87ba-4692-ae67-683bd0357e30\",\"account_id\":\"f2fc3e81-53a7-4dfb-96bf-8df8e90fc3b9\",\"from_id\":null,\"to_ids\":[\"8f6b3c89-43c3-4416-926d-410f65308315\"],\"cc_ids\":[],\"bcc_ids\":[]},\"type\":\"email\",\"object\":\"object_update\"}}",
#   "Timestamp" : "2015-06-03T18:14:12.891Z",
#   "SignatureVersion" : "1",
#   "Signature" : "FDtrma9GW4jjt53P2nPQ/zMGeNSU7ioIOxCQVyRA5jc9/Fe/cOGTaekJEIqBr4LQVccDlpDSmhvI6RxP9n+jyTqbsvu3j1++kosvXQYcTJV+jfZFR8J/0xcnaIzT7rhXXHJA8pzxC1xUdpbVeKrtQntEF3uOWXrv1bSvMn8rJn7lwa5nvg3FWySliUZUrBH0D3+k0xpcf3jImdBKHPWJLAl2Aqt08FXsTmjpCactkZ7JqxNbD9/8kiBIR9dtzkSO0A75S0Oq3Mm8qyiPkevBFqS75Qy/ASv4VIcD7rAuIZfNsgiIwxV2bZSr/mr5TzOm+UKB/hJAYKEDYnPGFvjIIw==",
#   "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-d6d679a1d18e95c2f9ffcf11f4f9e198.pem",
#   "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:242236168477:dev_message_bodies:9e11fdb6-189e-4ade-b38d-d50c88139e04"
# }
