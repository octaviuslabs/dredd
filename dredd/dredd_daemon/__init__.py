from event_scorer.email_message_scorer import EmailMessageScorer
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
import traceback
from daemon import Daemon
from mixins.multi_item_cycle_mixin import MultiItemCycleMixin
from exceptions import DaemonCycleError

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class DreddDaemon(MultiItemCycleMixin, Daemon):
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
                self.heartbeat.send_heartbeat()
                self._run_retryable_cycle()
                time.sleep(self.poll_interval)
                #TODO: It should wait until now to kill on ctr c
        except Exception as e:
            self.logging.critical(e)
            self.stop()

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=30000)
    def _run_retryable_cycle(self):
        try:
            cycle_outcome = self._run_cycle()
            if cycle_outcome:
                self.logging.info("Cycle Complete")
                return cycle_outcome
            else:
                raise
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logging.critical(str(exc_type))
            raise Exception("Retry")

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
