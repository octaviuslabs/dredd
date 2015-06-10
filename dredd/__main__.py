#!/usr/bin/env python
import logging
from logging.handlers import TimedRotatingFileHandler
from config import Configuration
from dredd_daemon import DreddDaemon
import sys
import os


def main(log):
    log.info("Running management script")
    configuration = Configuration()
    daemon = DreddDaemonconfiguration.poll_interval)
    if len(sys.argv) == 2:
    	if 'start' == sys.argv[1]:
    		daemon.start()
    	elif 'stop' == sys.argv[1]:
    		daemon.stop()
    	elif 'restart' == sys.argv[1]:
    		daemon.restart()
    	else:
    		print "Unknown command"
    		sys.exit(2)
    	sys.exit(0)
    else:
    	print "usage: %s start|stop|restart" % sys.argv[0]
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
