import sure
import redis
import json
import time
import random
from mem_store.email_message import EmailMessage
from mem_store.email_message.email_message_with_diff import EmailMessageWithDiff
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

from email_mocks import email_attrs



def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall

def sure_convert(statement):
    assert statement


def test_diffing_email_bodies_with_late_insert():
    flush_memory()

    for i in [0, 1, 3]:
        EmailMessageWithDiff(email_attrs[i]).save()

    late_email = EmailMessageWithDiff(email_attrs[2])
    yield sure_convert, (late_email.processed_text.raw).should.be.equal(u'this is the first sentence of the third email.')

    # late_email.processed_text should eq diff between 2 and 1

def test_diffing_with_nothing_to_diff():
    flush_memory()
    #
    initial_email = EmailMessageWithDiff(email_attrs[0])
    # processed_text.raw should eq email_attrs[0]["body"]
    yield sure_convert, (initial_email.processed_text.raw).should.be.equal(email_attrs[0]["body"])

def test_diff_body_only_in_processed_text():
    flush_memory()

    inserted_emails = []
    for message_hash in email_attrs:
        email_message = EmailMessageWithDiff(message_hash)
        email_message.save()
        inserted_emails.append(email_message)

        # Make sure the stored raw body is the same as what came from the message hash
        yield sure_convert, (email_message.body.raw).should.be.equal(message_hash["body"])

    for email_message in inserted_emails[1:4]:
        # Make sure that processed_text differs from the raw body in cases of diffs
        yield sure_convert, (email_message.processed_text.raw).should_not.be.equal(email_message.body.raw)
