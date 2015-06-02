import json
import urllib
import re
import time

class Request:
    def __init__(self, url):
        self.url = url

    def get_email_path(self):
        # response = json.load(urllib.urlopen(self.url))
        self.log("Polling Request")
        return "https://s3.amazonaws.com/vesper-stubs/email_object.json"

    def poll(self):
        self.log("Poll URL")
        response = urllib.urlopen(self.get_email_path())
        return json.load(response)

    def log(self, message):
        print str(int(time.time())) + " " + message
