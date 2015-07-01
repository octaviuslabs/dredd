from coordinator.q.dredd_message import DreddMessage
import json

class DreddEmailMessage(DreddMessage):
    url = None

    def __init__(self, bucket_name=None, path=None):
        self.set_url(bucket_name, path)
        super(DreddEmailMessage, self).__init__()

    def set_url(self, bucket_name, path):
        self.url = self.generate_url(bucket_name, path)

    def generate_url(self, bucket_name, path):
        return u'https://{0}.s3.amazonaws.com/{1}'.format(
            bucket_name,
            path)

    def get_body(self):
        return json.dumps({
            "Message": self.get_body_for_broadcast()
        })

    def get_body_for_broadcast(self):
        return json.dumps({"message": {
                "type": "email",
                "email": {
                    "url": self.url
                }
            },
        })
