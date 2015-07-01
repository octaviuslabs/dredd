import sure
import redis
import json
import time
import random
from mem_store.email_message import EmailMessage
from event_scorer.email_message_simple_property_scorer import EmailMessageSimplePropertyScorer
from mem_store.recommendation.thread_recommendation import ThreadRecommendation
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

target_account_id = 'this-is-the-accoundid'
target_thread_id = 'a-thread-of-email'
email_messages = [{ # Sent by self, first item
    "id": "this-be-my-id1",
    "account_id": target_account_id,
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": target_thread_id,
    "sent_at": "2015-02-23T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id",
    "from_id": "this-is-the-account-contact-id",
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
},{ # Sent by other, second item
    "id": "this-be-my-id2",
    "account_id": target_account_id,
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": target_thread_id,
    "sent_at": "2015-02-24T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id",
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
}]

# recommendation_key = "account:account_id:judgement:email_thread:judgement_name"


def sure_convert(statement):
    assert statement

def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall()

# def get_recommendations():
#     return redis.zrangebyscore(recommendation_key, '-inf', '+inf', withscores=True)


def test_is_last_message_in_thread():
    flush_memory()

    # Normal insert order
    email1 = EmailMessage(email_messages[0])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    email1.save()
    yield sure_convert, (test_subject1.is_last_message_in_thread()).should.be.equal(True)

    email2 = EmailMessage(email_messages[1])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    email2.save()
    yield sure_convert, (test_subject2.is_last_message_in_thread()).should.be.equal(True)

def test_is_last_message_in_thread_abnormal_insert_order():
    flush_memory()

    # Abnormal insert order
    email1 = EmailMessage(email_messages[1])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    email1.save()
    yield sure_convert, (test_subject1.is_last_message_in_thread()).should.be.equal(True)

    email2 = EmailMessage(email_messages[0])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    email2.save()
    yield sure_convert, (test_subject2.is_last_message_in_thread()).should.be.equal(False)

def test_self_sender_value():
    flush_memory()

    # First email is sent by self
    email1 = EmailMessage(email_messages[0])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    email1.save()
    yield sure_convert, (test_subject1.self_sender_value()).should.be.equal(1.0)

    # Second email is sent by other
    email2 = EmailMessage(email_messages[1])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    email2.save()
    yield sure_convert, (test_subject2.self_sender_value()).should.be.equal(0.0)

    pass


def test_judge_self_sender():
    flush_memory()

    # First email is sent by self so has a verdict of 1
    email1 = EmailMessage(email_messages[0])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    test_subject1.save()

    yield sure_convert, (
        ThreadRecommendation.get_recommendations(target_account_id, "self_sender")[0][1]).should.be.equal(1.0)

    # Second email is sent by other and verdict updates to 0
    email2 = EmailMessage(email_messages[1])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    test_subject2.save()

    yield sure_convert, (ThreadRecommendation.get_recommendations(target_account_id, "self_sender")[0][1]).should.be.equal(0.0)


def test_self_sender_value():
    flush_memory()

    email1 = EmailMessage(email_messages[0])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    yield sure_convert, (test_subject1.self_sender_value()).should.be.equal(1.0)

    email2 = EmailMessage(email_messages[1])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    yield sure_convert, (test_subject2.self_sender_value()).should.be.equal(0.0)


def test_judge_last_sent():
    flush_memory()

    # Normal insert order
    email1 = EmailMessage(email_messages[0])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    test_subject1.save()
    recommendation = ThreadRecommendation.get_recommendations(target_account_id, "last_sent")
    yield sure_convert, (recommendation[0][1]).should.be.equal(test_subject1.sent_at_to_f())

    email2 = EmailMessage(email_messages[1])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    test_subject2.save()
    recommendation = ThreadRecommendation.get_recommendations(target_account_id, "last_sent")
    yield sure_convert, (recommendation[0][1]).should.be.equal(test_subject2.sent_at_to_f())


def test_judge_last_sent_abnormal_insert_order():
    flush_memory()

    # Abnormal insert order
    email1 = EmailMessage(email_messages[1])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)
    test_subject1.save()
    recommendation = ThreadRecommendation.get_recommendations(target_account_id, "last_sent")
    yield sure_convert, (recommendation[0][1]).should.be.equal(test_subject1.sent_at_to_f())

    email2 = EmailMessage(email_messages[0])
    test_subject2 = EmailMessageSimplePropertyScorer(email2)
    test_subject2.save()
    recommendation = ThreadRecommendation.get_recommendations(target_account_id, "last_sent")
    yield sure_convert, (recommendation[0][1]).should.be.equal(test_subject1.sent_at_to_f())


def test_sent_at_to_f():
    flush_memory()

    email1 = EmailMessage(email_messages[1])
    test_subject1 = EmailMessageSimplePropertyScorer(email1)

    yield sure_convert, (test_subject1.sent_at_to_f()).should.be.equal(email1.sent_at.to_f())
