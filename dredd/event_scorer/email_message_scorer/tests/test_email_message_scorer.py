import sure
import redis
import json
import time
import random
from mem_lts_store.email_message import EmailMessage
from mem_lts_store.email_message.email_message_with_diff import EmailMessageWithDiff
from event_scorer.email_message_scorer import EmailMessageScorer
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

target_account_id = 'this-is-the-accoundid'
target_thread_id = 'a-thread-of-email'


email_messages = [{ # Expected score: 1
    "id": "this-be-my-id1",
    "account_id": target_account_id,
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": target_thread_id,
    "sent_at": "2015-02-23T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id0",
    "from_id": "id-for-from-contact",
    "to_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "cc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "bcc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "subject": "This Is The Subject Of The Email",
    "body": 'Hey dude. Did you see the question I asked you previously? Ok, awesome.'
},{
    "id": "this-be-my-id2",
    "account_id": target_account_id,
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": target_thread_id,
    "sent_at": "2015-02-24T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id1",
    "from_id": "id-for-from-contact",
    "to_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "cc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "bcc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "subject": "This Is The Subject Of The Email",
    "body": 'no scoreable features'
},{
    "id": "this-be-my-id3",
    "account_id": target_account_id,
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": target_thread_id,
    "sent_at": "2015-02-25T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id2",
    "from_id": "id-for-from-contact",
    "to_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "cc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "bcc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "subject": "This Is The Subject Of The Email",
    "body": 'Hey man. Did you get a chance to see my pokemons? Let me show you my pokemons!'
}]

recommendation_key = ":".join(['account', target_account_id, 'judgement', 'email_thread', 'question'])


def sure_convert(statement):
    assert statement

def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall()

def fetch_recommendations():
    return redis.zrangebyscore(recommendation_key, '-inf', '+inf', withscores=True)


class TestSubject(EmailMessageScorer):
    override_score_message_value = None

    def __init__(self, email_message):
        self.event_email_message = email_message

    def override_score_message(self, value):
        self.override_score_message_value = value

    def score_message(self, email_message):
        if self.override_score_message_value == None:
            return

        self.event_email_message.score_calculated = True
        email_message.score = self.override_score_message_value
        self.override_score_message_value = None
        return email_message.score

    def get_latest_message_diff(self):
        latest_message = TestEmailMessageWithDiff.load(self.get_later_items()[0])
        latest_message.diff_with_message(self.event_email_message)
        return latest_message

class UrlMappable:
    url_map = {
        "http://lts.meetvesper.com/id0": 0,
        "http://lts.meetvesper.com/id1": 1,
        "http://lts.meetvesper.com/id2": 2 }

    def lts_fetch(self, url):
        return json.dumps({'email': email_messages[self.url_map[url]]})


class TestEmailMessage(UrlMappable, EmailMessage):
    pass
class TestEmailMessageWithDiff(UrlMappable, EmailMessageWithDiff):
    pass

def test_normal_insert_order():
    flush_memory()

    insert_order = [0, 1, 2]
    expected_scores = [0.0, 1.0, 0.0]

    for index in insert_order:
        test_subject = TestSubject(TestEmailMessage(email_messages[index]))
        test_subject.override_score_message(expected_scores[index])
        test_subject.save()

        yield sure_convert, (fetch_recommendations()[0][1]).should.be.equal(expected_scores[index])

def test_abnormal_insert_order():
    flush_memory()

    insert_order = [2, 1, 0]
    given_scores = [2.0, 1.0, 12.0]
    expected_scores = [2.0, 1.0, 1.0]

    iteration_number = 0
    for index in insert_order:
        test_subject = TestSubject(TestEmailMessage(email_messages[index]))
        test_subject.override_score_message(given_scores[iteration_number])
        test_subject.save()

        yield sure_convert, (fetch_recommendations()[0][1]).should.be.equal(expected_scores[iteration_number])
        iteration_number += 1
