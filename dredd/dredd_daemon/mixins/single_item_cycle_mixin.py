from coordinator import Coordinator
import logging

class SingleItemCycleMixin(object):
    logging = logging.getLogger('dredd')
    def _run_cycle(self):
        coordinator = self.coordinator()
        task = coordinator.get_task()
        return self.process_task(task, coordinator)

    def coordinator(self):
        return Coordinator(self.config.q_name)

    def process_task(self, task, coordinator):
        scored_task = self._score_task(task)
        if scored_task.save():
            self.logging.info("Save")
            return coordinator.clean()
        return False
