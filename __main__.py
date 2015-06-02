from daemon import Daemon
from request import Request
import nltk
import pickle
from mem_store.email_message import EmailMessage
from config import Configuration
from retrying import retry

import sys, time

class Dredd:
    def __init__(self, queue_endpoint, poll_interval):
        self.endpoint = queue_endpoint
        self.poll_interval = poll_interval

    def run(self):
        self._log("Running...")
        request = Request(self.endpoint)
        while True:
            email = self._get_email(request)
            email = self._score_email(email)
            email.save()
            self._log("Saved " + str(email.id_) + " with a score of " + str(email.score))
            time.sleep(self.poll_interval)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def _get_email(self, request):
        response = request.poll()
        if not bool(response):
            message = self._log("No Email Found")
            raise Exception(message)
        email = EmailMessage(response)
        return email

    def _score_email(self, email):
        email.processed_text.classify_questions(self.classifier())
        email.add_feature('question_count', len(email.processed_text.questions))
        email.add_feature('non_question_count',  len(email.processed_text.non_questions))
        email.calculate_score()
        return email

    def classifier(self):
        try:
            return self.classifier_
        except AttributeError:
            file = open('./classified_output/naivebays_1433196824.pickle')
            self.classifier_ = pickle.load(file)
            file.close()
            return self.classifier_

    def _log(self, message):
        print str(int(time.time())) + " " + message

if __name__ == "__main__":
    config = Configuration()
    daemon = Dredd(config.queue_endpoint, config.poll_interval)
    daemon.run()
