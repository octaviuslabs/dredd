from daemon import Daemon
from request import Request
import nltk
import pickle
from mem_store.email_message import EmailMessage

import sys, time

class Dredd:
    def __init__(self, poll_interval):
        self.poll_interval = poll_interval
        self.endpoint = "the-endpoint"

    def run(self):
        print "Running"
        request = Request(self.endpoint)
        while True:
            res = request.poll()
            email = self.build_email(res)
            email.processed_text.classify_questions(self.classifier())
            email.add_feature('question_count', len(email.processed_text.questions))
            email.add_feature('non_question_count',  len(email.processed_text.non_questions))
            email.calculate_score()
            email.save()
            print email.to_json()
            time.sleep(self.poll_interval)

    def build_email(self, attrs):
        return EmailMessage(attrs)

    def classifier(self):
        try:
            return self.classifier_
        except AttributeError:
            file = open('./classified_output/naivebays_1433196824.pickle')
            self.classifier_ = pickle.load(file)
            file.close()
            return self.classifier_


if __name__ == "__main__":
    daemon = Dredd(10)
    daemon.run()
