import sure
import redis
import json
import time
import random
from mem_store.init_status import InitStatus
from nose_focus import focus
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

def sure_convert(statement):
    assert statement


def flush_memory():
    return redis.flushall()

def teardown_func():
    redis.flushall()


def test_should_init_true():
    flush_memory()
    init_status = InitStatus()

    yield sure_convert, (init_status.should_init()).should.be.equal(True)


def test_should_init_false():
    flush_memory()
    redis.setnx("init_status:started", time.time())
    init_status = InitStatus()

    yield sure_convert, (init_status.should_init()).should.be.equal(False)
