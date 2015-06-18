from config import Configuration
from daemon import Daemon
import time
import logging
import os, sys
from daemon import Daemon
from mem_store.init_status import InitStatus
from q_primer import QPrimer

# Daemon pattern found http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
class DreddPrimerDaemon(Daemon):
    config = Configuration()
    logging = logging.getLogger('dredd')

    def __init__(self):
        super(DreddPrimerDaemon, self).__init__('/tmp/dredd_primer.pid')

    def start(self):
        self.logging.info("Starting Dredd Primer")
        init_status = InitStatus()
        if init_status.should_init():
            self.logging.info("Primer is needed. Starting Primer.")
            try:
                super(DreddPrimerDaemon, self).start()
            except Exception as e:
                self.logging.info(e)

        else:
            self.logging.info("Primer is not needed. Stopping Primer Daemon.")
            self.self_clean_stop()

    # Cleanly stop the daemon from its own process (remove the pid file so other
    #   launches don't believe the daemon is still running, and then exit with
    #   status 0)
    def self_clean_stop(self):
        self.logging.info("Stopping Dredd Primer")

        try:
            self.delpid()
        except:
            pass
        sys.exit(0)

    def stop(self):
        # Signal subsequent processes that the init process did not complete
        #   properly
        init_status = InitStatus()
        init_status.delete_init()


    def run(self):
        self.logging.info("Primer is running")

        try:
            primer = QPrimer()
            primer.prime()
        except Exception as e:
            self.logging.critical("Error attempting to prime: {0}".format(e))

        # Set the finish time in the store 
        init_status = InitStatus()
        init_status.set_finished()

        self.logging.info("Dredd Primer Finished. Stopping.")
        self.self_clean_stop()
