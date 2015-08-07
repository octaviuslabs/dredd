import sure
import redis
import json
import time
import random
from lts_store import Base as LtsStoreBase

from mocks import example_data


class TestSubject(LtsStoreBase):
    def url(self):
        return "test url"

    def lts_fetch(self, url):
        return example_data

def sure_convert(statement):
    assert statement

def test_lts_store():
    pass

def test_lts_load():
    example_data_hash = json.loads(example_data)
    tester = TestSubject()
    yield sure_convert, (tester.lts_load('test')).should.be.equal(example_data_hash['test'])


def test_lts_data_hash():
    example_data_hash = json.loads(example_data)
    tester = TestSubject()
    yield sure_convert, (tester.lts_data_hash()).should.be.equal(example_data_hash)

def test_lts_data():
    tester = TestSubject()
    yield sure_convert, (tester.lts_data()).should.be.equal(example_data)
