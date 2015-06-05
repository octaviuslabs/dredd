from coordinator import Coordinator
import nltk
import pickle
from config import Configuration
from daemon import Daemon
from heartbeat import Heartbeat
from retrying import retry
import time
import logging
import os

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class Dredd:
    config = Configuration()
    def __init__(self, queue_endpoint, poll_interval):
        self.endpoint = queue_endpoint
        self.poll_interval = poll_interval
        logging.info("Dredd is running...")

    def run(self):
        heartbeat = Heartbeat()
        while True:
            self._run_cycle(heartbeat)
            time.sleep(self.poll_interval)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=30000)
    def _run_cycle(self, heartbeat):
        try:
            heartbeat.send_heartbeat()
            coordinator = Coordinator(self.config.q_name)
            task = coordinator.get_task()
            if bool(task):
                task = self._score_task(task)
                if task.save():
                    coordinator.clean()
            # It should wait until now to kill
            time.sleep(self.poll_interval)
        except Exception as e:
            logging.critical(e)


    def start(self):
        logging.info("Starting Dredd")
        self.run()

    def stop(self):
        logging.info("Stopping Dredd")

    def _score_task(self, task):
        task.processed_text.classify_questions(self.classifier())
        task.add_feature('question_count', len(task.processed_text.questions))
        task.add_feature('non_question_count',  len(task.processed_text.non_questions))
        score = task.calculate_score()
        logging.info(str(score))
        return task

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
