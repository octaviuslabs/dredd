import sure
import redis
import json
import time
from mem_store.email_message import EmailMessage
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

email_attrs = {
    "id": "this-be-my-id",
    "account_id": "this-is-the-accoundid",
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
    redis.flushall

def teardown_func():
    redis.flushall

def test():
    flush_memory
    email = EmailMessage(email_attrs)
    yield sure_convert, (email.id_).should.be.equal(email_attrs["id"])
    yield sure_convert, (email.account_id).should.be.equal(email_attrs["account_id"])
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

def test_saving():
    flush_memory
    email = EmailMessage(email_attrs)
    email.score = 50
    email.save()
    # Recommendation Save Test
    reco_listing = json.dumps({ "type": "email_thread", "id": email_attrs["thread_id"], "score": 50})
    key = ":".join(["recommendations",  email_attrs["account_id"]])
    yield sure_convert, (redis.zrangebyscore(key, 50, 50)).should.be.equal([reco_listing])
    # how do you overwite a recommendation & make sure its unique

    # Thread Add Test
    key = ":".join(["email_threads",  email_attrs["account_id"], email_attrs["thread_id"]])
    email_time = email_attrs["sent_at"]
    email_time = time.strptime(email_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    email_time = time.mktime(email_time)
    yield sure_convert, (redis.zrangebyscore(key, email_time, email_time)).should.be.equal([email_attrs["id"]])

    # Save json or_url in emails
    key = ":".join(["emails", email_attrs["id"]])
    yield sure_convert, (json.loads(redis.get(key))).should.be.equal(email_attrs)

# It should know what to do if it gets null values for the attrs

# Save questions in question?
# key = ":".join(["questions", email_attrs["id"]])
# (redis.lget(key)).should.be.equal(["this-is-a-question-man1", "this-is-a-question-man2"])
# It should have a error state???

# it should be able to fetch an object and build its self
