from coordinator.multi_task_coordinator import MultiTaskCoordinator
import sure

def sure_convert(statement):
    assert statement

class MockMessage:
    account_id = "this-is-account-id"
    def parsed_message(self):
        return {"type": "email"}

class MockTask:
    def __init__(self, id_="mock-task-id", account_id="account-id"):
        self.id_ = id_
        self.account_id = account_id

class MockQ:
    def fetch_messages(self, number):
        msgs = list()
        for i in range(number):
            msgs.append(MockMessage())
        return msgs

    def remove_message(self, message):
        return True


class DoubleCoordinator(MultiTaskCoordinator):
    def q(self):
        return MockQ()

    def _fetch_task_data(self, msg):
        return MockTask()

def test_get_tasks():
    coordinator = DoubleCoordinator("q-name")
    tasks = coordinator.get_tasks(3)
    sure_convert((len(tasks)).should.be.equal(3))

def test_clean_tasks():
    coordinator = DoubleCoordinator("q-name")
    tasks = coordinator.get_tasks(3)
    subject = coordinator.clean(tasks[0])
    sure_convert(subject.should.be.equal(True))
