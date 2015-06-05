#!/usr/bin/env python
import logging
from config import Configuration
from dredd import Dredd
import sys

def main():
    logging.info("Loading Service")
    configuration = Configuration()
    daemon = Dredd(configuration.queue_endpoint, 3)
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s %(asctime)s: %(message)s')
    main()
