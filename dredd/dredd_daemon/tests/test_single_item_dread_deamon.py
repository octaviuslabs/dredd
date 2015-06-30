import sure
from nose.tools import assert_raises
from nose.tools import raises
from dredd_daemon import DreddDaemon
from dredd_daemon.mixins.single_item_cycle_mixin import SingleItemCycleMixin
from nose_focus import focus

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
    "body": "This is the body of the email. This is the second sentence of the first email."
}

def sure_convert(statement):
    assert statement

class MockObj:
    def __init__(self, attrs={}):
        self.save_status = attrs.get("save", False)
        self.clean_status = attrs.get("clean", False)

    def clean(self):
        return self.clean_status

    def save(self):
        return self.save_status

    def get_task(self):
        return MockObj({"save": True})

class DoubleDaemon(SingleItemCycleMixin, DreddDaemon):
    def _score_task(self, task):
        return task

def test__run_cycle_success():
    class CycleDaemon(DoubleDaemon):
        def coordinator(self):
            return MockObj({"clean": True})
    deamon = CycleDaemon(1)
    yield sure_convert, (deamon._run_cycle()).should.be.equal(True)

def test_process_task_success():
    task_mock = MockObj({"save": True})
    coordinator_mock = MockObj({"clean": True})
    deamon = DoubleDaemon(1)
    yield sure_convert, (deamon.process_task(task_mock, coordinator_mock)).should.be.equal(True)

def test_process_task_task_failure():
    task_mock = MockObj({"save": False})
    coordinator_mock = MockObj({"clean": True})
    deamon = DoubleDaemon(1)
    yield sure_convert, (deamon.process_task(task_mock, coordinator_mock)).should.be.equal(False)

def test_process_task_coordinator_failure():
    task_mock = MockObj({"save": True})
    coordinator_mock = MockObj({"clean": False})
    deamon = DoubleDaemon(1)
    yield sure_convert, (deamon.process_task(task_mock, coordinator_mock)).should.be.equal(False)
