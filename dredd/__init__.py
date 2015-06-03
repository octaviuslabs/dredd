from request import Request
import nltk
import pickle
from mem_store.email_message import EmailMessage
from config import Configuration
from retrying import retry
from daemon import Daemon
from heartbeat import Heartbeat
import time
import logging
import os

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class Dredd:
    def __init__(self, queue_endpoint, poll_interval):
        pid = '/tmp/dredd.pid'
        self.endpoint = queue_endpoint
        self.poll_interval = poll_interval
        logging.info("Dredd is running...")
        # super(Dredd, self).__init__('/tmp/dredd.pid')

    def run(self):
        request = Request(self.endpoint)
        heartbeat = Heartbeat()
        while True:
            heartbeat.send_heartbeat()
            email = self._get_email(request)
            email = self._score_email(email)
            email.save()
            time.sleep(self.poll_interval)

    def start(self):
        logging.info("Starting Dredd")
        self.run()
        # super(Dredd, self)

    def stop(self):
        logging.info("Stopping Dredd")
        super(Dredd, self)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def _get_email(self, request):
        response = request.poll()
        if not bool(response):
            message = logging.info("No Email Found")
            raise Exception(message)
        email = EmailMessage(response)
        return email

    def _score_email(self, email):
        logging.info("Scoring Email " + email.id_)
        email.processed_text.classify_questions(self.classifier())
        email.add_feature('question_count', len(email.processed_text.questions))
        email.add_feature('non_question_count',  len(email.processed_text.non_questions))
        email.calculate_score()
        return email

    def classifier(self):
        try:
            return self.classifier_
        except AttributeError:
            classifier_location = '../classified_output/naivebays_1433295569.pickle'
            classifier_location = os.path.join(os.path.dirname(__file__), classifier_location)
            file = open(classifier_location)
            self.classifier_ = pickle.load(file)
            file.close()
            return self.classifier_
