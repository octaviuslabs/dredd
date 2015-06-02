import json
import urllib
import re
import time

class Request:
    def __init__(self, url):
        self.url = url
        self.retries = 0

    def get_email_path(self):
        self._log("Polling Queue")
        return "https://s3.amazonaws.com/vesper-stubs/email_object.json"

    def poll(self):
        self._log("Poll URL")
        email_path = self.get_email_path()
        response = urllib.urlopen(email_path)
        response = self._serialize_response(response)
        # it should return empty response if nothing came back
        return response

    def _log(self, message):
        print str(int(time.time())) + " " + message

    def _serialize_response(self, response):
        return json.load(response)
