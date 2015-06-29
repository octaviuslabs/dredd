from coordinator import Coordinator
from coordinator.task_stack import TaskStack
from coordinator.task_pair import TaskPair

class MultiTaskCoordinator(Coordinator):
    task_pairs = TaskStack()

    def clean(self, task_pair):
        self.logger.info("Cleaning Message")
        self.clean_internal_init_status(task_pair)
        return self.q().remove_message(task_pair.message)

    def clean_internal_init_status(self, task_pair):
        return task_pair.init_status.finish_item()

    def get_tasks(self, stack_size=1):
        self.messages = self.q().fetch_messages(stack_size)
        if len(self.messages) <= 0:
            self.logger.info("No messages found")
            return self.task_pairs
        for message in self.messages:
            task = self._fetch_task_data(message.parsed_message())
            task_pair = TaskPair(message, task)
            self.task_pairs.append(task_pair)
        return self.task_pairs
