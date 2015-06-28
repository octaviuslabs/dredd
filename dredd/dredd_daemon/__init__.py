from coordinator import Coordinator
from event_scorer.email_message_scorer import EmailMessageScorer
from coordinator import NoMessage
import nltk
import pickle
from config import Configuration
from daemon import Daemon
from heartbeat import Heartbeat
from retrying import retry
import time
import logging
import os
import sys
from daemon import Daemon

class DaemonCycleError(Exception):
    pass

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class DreddDaemon(Daemon):
    config = Configuration()
    logging = logging.getLogger('dredd')
    classifier_filename = 'naivebays_1433295569.pickle'

    def __init__(self, poll_interval):
        super(DreddDaemon, self).__init__('/tmp/dredd.pid')
        self.poll_interval = poll_interval
        self.daemon_location = os.path.abspath(__file__)
        self.heartbeat = Heartbeat()

    def run(self):
        try:
            self.logging.info("Dredd is running...")
            self.get_classifier()
            while True:
                self._run_cycle()
                time.sleep(self.poll_interval)
                # It should wait until now to kill on ctr c
        except Exception as e:
            self.logging.critical(e)
            self.stop()

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=30000)
    def _run_cycle(self):
        try:
            self.heartbeat.send_heartbeat()
            coordinator = self.coordinator()
            task = coordinator.get_task()
            return self.process_task(task, coordinator)
        except NoMessage:
            raise DaemonCycleError
        except:
            e = sys.exc_info()[0]
            self.logging.critical(e)
            raise DaemonCycleError
        return False

    def coordinator(self):
        return Coordinator(self.config.q_name)

    def process_task(self, task, coordinator):
        scored_task = self._score_task(task)
        if scored_task.save():
            return coordinator.clean()
        return False

    def start(self):
        self.logging.info("Starting Dredd")
        super(DreddDaemon, self).start()

    def stop(self):
        self.logging.info("Stopping Dredd")
        super(DreddDaemon, self).stop()

    def _score_task(self, task):
        return EmailMessageScorer(task, self.get_classifier())


    def get_classifier(self):
        try:
            return self.classifier_
        except AttributeError:
            classifier_location = os.path.abspath(os.path.join(self.daemon_location, os.pardir, os.pardir, os.pardir, "classified_output", self.classifier_filename))
            file = open(classifier_location)
            self.classifier_ = pickle.load(file)
            file.close()
            return self.classifier_
