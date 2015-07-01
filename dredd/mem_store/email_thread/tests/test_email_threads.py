import sure
import redis
import json
import time
import random
from mem_store.email_message import EmailMessage
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

target_account_id = 'this-is-the-accoundid'

email_messages = [{ # Expected score: 1
    "id": "this-be-my-id1",
    "account_id": "this-is-the-accoundid",
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": "a-thread-of-email",
    "sent_at": "2015-02-23T21:22:48.000Z",
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
    "body": 'Hey dude. Did you see the question I asked you previously? Ok, awesome.'
},{
    "id": "this-be-my-id2",
    "account_id": "this-is-the-accoundid",
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": "a-thread-of-email",
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
},{
    "id": "this-be-my-id3",
    "account_id": "this-is-the-accoundid",
    "account_contact_id": "this-is-the-account-contact-id",
    "thread_id": "a-thread-of-email",
    "sent_at": "2015-02-25T21:22:48.000Z",
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
    "body": 'Hey man. Did you get a chance to see my pokemons? Let me show you my pokemons!'
}]

contrived_scores = [1, 0, 2]
recommendation_key = ":".join(['account', target_account_id, 'judgement', 'email_thread', 'question'])

# Score 1: [0, 1, 2] :: results: 1, 0, 2
# Score 2: [0, 2, 1] :: results: 1, 2, 2


def sure_convert(statement):
    assert statement

def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall()

def test_get_items_after():
    flush_memory()

    email = EmailMessage(email_messages[2])
    email.save()
    test_data = len(email.thread.get_items_after(email.sent_at.to_f()))
    yield sure_convert, test_data.should.be.equal(0)

    email = EmailMessage(email_messages[1])
    email.save()
    test_data = len(email.thread.get_items_after(email.sent_at.to_f()))
    yield sure_convert, test_data.should.be.equal(1)

    email = EmailMessage(email_messages[0])
    email.save()
    test_data = len(email.thread.get_items_after(email.sent_at.to_f()))
    yield sure_convert, test_data.should.be.equal(2)


def test_normal_run():
    flush_memory()

    insert_order = [0, 1, 2]
    expected_results = [1.0, 0.0, 2.0]

    iteration_number = 0
    for index in insert_order:
        email = EmailMessage(email_messages[index])
        email.score = contrived_scores[index]
        email.score_calculated = True
        email.save()
        thread_recommendation = redis.zrangebyscore(recommendation_key, '-inf', '+inf', withscores=True)
        yield sure_convert, thread_recommendation.should.be.equal([
            (email.thread.storage_key,
            expected_results[iteration_number])
        ])
        iteration_number += 1

def test_abnormal_insert_order():
    flush_memory()

    insert_order = [0, 2, 1]
    expected_results = [1.0, 2.0, 2.0]

    iteration_number = 0
    for index in insert_order:
        email = EmailMessage(email_messages[index])
        email.score = contrived_scores[index]
        email.score_calculated = True
        email.save()
        thread_recommendation = redis.zrangebyscore(recommendation_key, '-inf', '+inf', withscores=True)
        yield sure_convert, thread_recommendation.should.be.equal([
            (email.thread.storage_key,
            expected_results[iteration_number])
        ])
        iteration_number += 1
