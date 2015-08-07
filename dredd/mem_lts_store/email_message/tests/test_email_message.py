import sure
import redis
import json
import time
import random
from mem_lts_store.email_message import EmailMessage
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

mock_lts_data = """{
  "email": {
    "id": "8XgeNrRyaYBQp4Pw9lUOzDOd5EqjLKW01JGm",
    "sent_at": "2015-01-23T21:58:17.000Z",
    "url": "https://vesper-lts-development.s3.amazonaws.com/accounts/1/threads/243d6587-bdd3-4b69-b34d-f444c077eb94/emails/231070d9-ff22-49d0-b36f-b5136ff57f88.json",
    "deleted_at": null,
    "thread_id": "0QZn6pqbvkOJy1oV0JfM9DBjmY53GxX7gaWz",
    "account_id": "pNO4693Q85aRgdjDYJhowXL0ZkGP1BWybYMv",
    "account_contact_id": "4rLN8yX9eYnZRQEAB6S1aAv0JdgMlo6jGxzB",
    "from_id": "EzNRMqgKrbOZoXPAKRSbnVQd41va9LGk0pBl",
    "to_ids": [
      "4rLN8yX9eYnZRQEAB6S1aAv0JdgMlo6jGxzB"
    ],
    "cc_ids": [],
    "bcc_ids": [],
    "subject": "Invitation to collaborate on res-creative-adcreation",
    "body": "test body!"
  },
  "type": "email",
  "object": "object_update"
}"""

mock_lts_data_without_body = """{
  "email": {
    "id": "8XgeNrRyaYBQp4Pw9lUOzDOd5EqjLKW01JGm",
    "sent_at": "2015-01-23T21:58:17.000Z",
    "url": "https://vesper-lts-development.s3.amazonaws.com/accounts/1/threads/243d6587-bdd3-4b69-b34d-f444c077eb94/emails/231070d9-ff22-49d0-b36f-b5136ff57f88.json",
    "deleted_at": null,
    "thread_id": "0QZn6pqbvkOJy1oV0JfM9DBjmY53GxX7gaWz",
    "account_id": "pNO4693Q85aRgdjDYJhowXL0ZkGP1BWybYMv",
    "account_contact_id": "4rLN8yX9eYnZRQEAB6S1aAv0JdgMlo6jGxzB",
    "from_id": "EzNRMqgKrbOZoXPAKRSbnVQd41va9LGk0pBl",
    "to_ids": [
      "4rLN8yX9eYnZRQEAB6S1aAv0JdgMlo6jGxzB"
    ],
    "cc_ids": [],
    "bcc_ids": [],
    "subject": "Invitation to collaborate on res-creative-adcreation"
    },
  "type": "email",
  "object": "object_update"
}"""

mock_init_data = json.loads(mock_lts_data_without_body)["email"]


class TestSubject(EmailMessage):
    def lts_fetch(self, url):
        return mock_lts_data

def sure_convert(statement):
    assert statement

def test_loading_body():
    expected_body = json.loads(mock_lts_data)['email']['body']
    tester = TestSubject(mock_init_data)
    yield sure_convert, (tester.body.raw).should.be.equal(expected_body)
