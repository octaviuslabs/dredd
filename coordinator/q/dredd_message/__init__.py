import logging
import json
from boto.sqs.message import RawMessage

class DreddMessage(RawMessage):
    def parsed_body(self):
        message = json.loads(self.get_body())
        message["Message"] = json.loads(message.get("Message", ""))
        return message

    def parsed_message(self):
        return self.parsed_body().get("Message", {}).get("message", {})

    def is_valid(self):
        return bool(self.parsed_message().get("email", None))
