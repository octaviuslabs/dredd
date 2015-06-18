#!/usr/bin/env python
import logging
from logging.handlers import TimedRotatingFileHandler
from config import Configuration
from dredd_daemon import DreddDaemon
from dredd_primer_daemon import DreddPrimerDaemon

import sys
import os


def main(log):
    log.info("Running management script")
    configuration = Configuration()


    if len(sys.argv) == 3:
        log.info("Launching daemon: %s" % sys.argv[1])
        daemon = None
        if sys.argv[1] == 'judge':
            daemon = DreddDaemon(configuration.poll_interval)
        elif sys.argv[1] == 'prime':
            daemon = DreddPrimerDaemon()
        else:
            print "Unknown daemon (use 'prime' to initialize or 'judge' to run)"
            sys.exit(2)

        launch_daemon(daemon, log)

    	sys.exit(0)
    else:
    	print "usage: %s prime|judge start|stop|restart" % sys.argv[0]
    	sys.exit(2)

def launch_daemon(daemon, log):
    log.info("Launching daemon with parameter: %s" % sys.argv[2])
    if 'start' == sys.argv[2]:
        daemon.start()
    elif 'stop' == sys.argv[2]:
        daemon.stop()
    elif 'restart' == sys.argv[2]:
        daemon.restart()
    else:
		print "Unknown command"
		sys.exit(2)



def assure_path_exists(path="~/dredd_logs"):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == "__main__":
    logger = logging.getLogger('dredd')
    logger.setLevel(logging.INFO)
    log_file = assure_path_exists("~/dredd_logs") + "/current.log"
    file_handeler = TimedRotatingFileHandler(log_file, when="midnight", utc=True)
    log_format = logging.Formatter('%(levelname)s %(asctime)s: %(message)s')
    file_handeler.setFormatter(log_format)
    logger.addHandler(file_handeler)

    main(logger)
