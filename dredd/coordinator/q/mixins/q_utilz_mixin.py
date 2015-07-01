import logging
class QutilzMixin(object):
    logging = logging.getLogger('dredd')

    def remove_message(self, message):
        self.logging.info("Deleting message")
        return self.q().delete_message(message)
