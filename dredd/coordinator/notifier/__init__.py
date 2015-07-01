import boto.sns
import json
import logging
from config import Configuration

class Notifier(object):
    topic_arns = {}
    logging = logging.getLogger('dredd')
    config = Configuration()


    def notifier_client(self):
        try:
            return self.notifier_client_
        except AttributeError as err:
            self.notifier_client_ = boto.sns.connect_to_region(
                self.config.q_region,
                aws_access_key_id=self.config.aws_access_key,
                aws_secret_access_key=self.config.aws_secret_access_key)
            return self.notifier_client_

    def get_topic_arn(self, topic):
        full_topic_name = self.build_topic_name(topic)
        try:
            self.logging.info(self.topic_arns[full_topic_name])
            return self.topic_arns[full_topic_name]
        except:
            raw_topics = self.notifier_client().get_all_topics()['ListTopicsResponse']['ListTopicsResult']['Topics']
            self.topic_arns = { item['TopicArn'].split(":")[5] : item['TopicArn'] for item in raw_topics}

            self.logging.info(self.topic_arns[full_topic_name])
            return self.topic_arns[full_topic_name]

    def build_topic_name(self, topic):
        return "%s_%s" % (self.config.pub_sub_prefix, topic)

    def post_message(self, topic, message):
        try:
            message = self.notifier_client().publish(
                target_arn=self.get_topic_arn(topic),
                message=message.get_body_for_broadcast())
        except Exception as err:
            self.logging.critical(err)
            raise

        return message
