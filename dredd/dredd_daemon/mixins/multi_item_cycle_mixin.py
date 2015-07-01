import logging
from coordinator.multi_task_coordinator import MultiTaskCoordinator
from config import Configuration
class MultiItemCycleMixin(object):
    logging = logging.getLogger('dredd')
    config = Configuration()

    def _run_cycle(self):
        coordinator = self.coordinator()
        task_stack = coordinator.get_tasks(self.config.q_batch_size)
        result = True
        for task_pair in task_stack:
            self.logging.info("Processing Task Pair")
            result = (result and self.process_task(task_pair) and coordinator.clean(task_pair))
        return result

    def coordinator(self):
        return MultiTaskCoordinator(self.config.q_name)

    def process_task(self, task_pair):
        scored_task = self._score_task(task_pair.task)
        return scored_task.save()
