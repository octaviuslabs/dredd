import time


def log(message):
    logger.info(message)
    print str(int(time.time())) + " " + message
