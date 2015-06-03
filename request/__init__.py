import json
import urllib
import re
import time
import logging

class Request:
    def __init__(self, url):
        self.url = url
        self.retries = 0

    def _get_message(self):
        try:
            logging.info("Polling Queue")
            message = {
                "url": "https://s3.amazonaws.com/vesper-stubs/email_object.json"
            }
            return message
        except:
            logging.warn("There was an error pulling from the queue")

    def poll(self):
        message = self._get_message()
        email = self._get_email_data(message["url"])
        return email


    def _get_email_data(self, location):
        try:
            logging.info("Getting email from: " + str(location))
            response = urllib.urlopen(location)
            email = self._serialize_response(response)
            return email
        except:
            logging.warn("There was an error pulling email data from" + str(location))


    def _serialize_response(self, response):
        # it should return empty response if nothing came back
        return json.load(response)
