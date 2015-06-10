import sure
import redis
import json
import time
import random
from mem_store.email_message import EmailMessage
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

email_attrs = {
    "id": "this-be-my-id",
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
    "body": "This is the body of the email"
}

def sure_convert(statement):
    assert statement

#flush db
def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall

def test_building():
    flush_memory()
    email = EmailMessage(email_attrs)
    yield sure_convert, (email.id_).should.be.equal(email_attrs["id"])
    yield sure_convert, (email.account_id).should.be.equal(email_attrs["account_id"])
    yield sure_convert, (email.account_contact_id).should.be.equal(email_attrs["account_contact_id"])
    yield sure_convert, (email.thread.id_).should.be.equal(email_attrs["thread_id"])
    yield sure_convert, (email.thread.account_id).should.be.equal(email_attrs["account_id"])
    yield sure_convert, (email.sent_at.to_s()).should.be.equal(email_attrs["sent_at"])
    yield sure_convert, (email.url).should.be.equal(email_attrs["url"])
    yield sure_convert, (email.from_.id_).should.be.equal(email_attrs["from_id"])
    contact_ids = [contact.id_ for contact in email.to]
    yield sure_convert, (contact_ids).should.be.equal(email_attrs["to_ids"])
    contact_ids = [contact.id_ for contact in email.cc]
    yield sure_convert, (contact_ids).should.be.equal(email_attrs["cc_ids"])
    contact_ids = [contact.id_ for contact in email.bcc]
    yield sure_convert, (contact_ids).should.be.equal(email_attrs["bcc_ids"])
    yield sure_convert, (email.subject).should.be.equal(email_attrs["subject"])
    yield sure_convert, (email.body.raw).should.be.equal(email_attrs["body"])

def test_empty_body():
    empty_body = email_attrs
    empty_body["body"] = ""
    email = EmailMessage(email_attrs)
    yield sure_convert, (email.body.raw).should.be.equal("")

def test_saving():
    flush_memory()
    random_score = "%.4f"%(random.random()*100000)
    email = EmailMessage(email_attrs)
    email.score = random_score
    email.save()
    # Recommendation Save Test
    reco_listing = ":".join(["account", email_attrs["account_id"], "email_thread", email_attrs["thread_id"]])
    key = ":".join(["recommendations",  email_attrs["account_id"]])
    yield sure_convert, (redis.zrangebyscore(key, random_score, random_score)).should.be.equal([reco_listing])
    # Thread Add Test
    key = ":".join(["account", email_attrs["account_id"], "email_thread", email_attrs["thread_id"]])
    email_time = email_attrs["sent_at"]
    email_time = time.strptime(email_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    email_time = time.mktime(email_time)
    yield sure_convert, (redis.zrangebyscore(key, email_time, email_time)).should.be.equal([email_attrs["id"]])

    # Save json or_url in emails
    key = ":".join(["account", email_attrs["account_id"], "email", email_attrs["id"]])
    yield sure_convert, (json.loads(redis.get(key))).should.be.equal(email_attrs)

def test_inserting_old_thread():
    flush_memory()

    email2_attrs = email_attrs.copy()
    email2_attrs["id"] = "id-of-email-2"
    email2_attrs["sent_at"] = "2015-03-01T21:22:48.000Z"
    email2 = EmailMessage(email2_attrs)
    email2.score = float(75)
    email2.save()

    email1 = EmailMessage(email_attrs)
    email1.score = float(50)
    email1.save()
    key = ":".join(["recommendations",  email_attrs["account_id"]])
    reco_listing = ":".join(["account", email_attrs["account_id"], "email_thread", email_attrs["thread_id"]])
    yield sure_convert, (redis.zrangebyscore(key, "-inf", "+inf", withscores=True)).should.be.equal([(reco_listing, float(75))])

def test_inserting_new_thread():
    flush_memory()

    email1 = EmailMessage(email_attrs)
    email1.score = float(50)
    email1.save()

    email2_attrs = email_attrs.copy()
    email2_attrs["id"] = "id-of-email-2"
    email2_attrs["sent_at"] = "2015-03-01T21:22:48.000Z"
    email2 = EmailMessage(email2_attrs)
    email2.score = float(2)
    email2.save()

    key = ":".join(["recommendations",  email_attrs["account_id"]])
    reco_listing = ":".join(["account", email_attrs["account_id"], "email_thread", email_attrs["thread_id"]])
    yield sure_convert, (redis.zrangebyscore(key, "-inf", "+inf", withscores=True)).should.be.equal([(reco_listing, float(2))])
