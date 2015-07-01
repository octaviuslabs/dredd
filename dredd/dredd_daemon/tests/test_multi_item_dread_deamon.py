import sure
from nose.tools import assert_raises
from nose.tools import raises
from dredd_daemon import DreddDaemon
from dredd_daemon.mixins.multi_item_cycle_mixin import MultiItemCycleMixin
from nose_focus import focus

### Mocks
class Echo(object):
    def __init__(self, return_value):
        self.return_value = return_value

class TaskMock(Echo):
    def save(self):
        return self.return_value

class MockTaskPair(Echo):
    def __init__(self, return_value):
        super(MockTaskPair, self).__init__(return_value)
        self.task = self.task_()

    def task_(self):
        return TaskMock(self.return_value)

class MockCoordiantor(object):
    def get_tasks(self, size):
        pairs = list()
        for i in range(size):
            pairs.append(MockTaskPair(True))
        return pairs

    def clean(self, task_pair):
        return True

class DoubleDaemon(MultiItemCycleMixin):
    def _score_task(self, task):
        return task

    def coordinator(self):
        return MockCoordiantor()

### TESTS
def sure_convert(statement):
    assert statement

def test__run_cycle_success():

    class CycleDaemon(DoubleDaemon):
        def process_task(self, task_pair):
            return True

    deamon = CycleDaemon()
    yield sure_convert, (deamon._run_cycle()).should.be.equal(True)

def test__run_cycle_process_task_failure():

    class CycleDaemon(DoubleDaemon):
        def process_task(self, task_pair):
            return False

    deamon = CycleDaemon()
    yield sure_convert, (deamon._run_cycle()).should.be.equal(False)

def test__run_cycle_clean_failure():
    class FailureCoord(MockCoordiantor):
        def clean(self, task_pair):
            return False

    class CycleDaemon(DoubleDaemon):
        def coordinator(self):
            return FailureCoord()

        def process_task(self, task_pair):
            return True

    deamon = CycleDaemon()
    yield sure_convert, (deamon._run_cycle()).should.be.equal(False)


def test__run_cycle_clean_and_process_task_failure():
    class FailureCoord(MockCoordiantor):
        def clean(self, task_pair):
            return False

    class CycleDaemon(DoubleDaemon):
        def coordinator(self):
            return FailureCoord()

        def process_task(self, task_pair):
            return False

    deamon = CycleDaemon()
    yield sure_convert, (deamon._run_cycle()).should.be.equal(False)


def test_process_task_success():
    deamon = DoubleDaemon()
    task_pair = MockTaskPair(True)
    subject = deamon.process_task(task_pair)
    yield sure_convert, (subject).should.be.equal(True)

def test_process_task_task_failure():
    deamon = DoubleDaemon()
    task_pair = MockTaskPair(False)
    subject = deamon.process_task(task_pair)
    yield sure_convert, (subject).should.be.equal(False)
