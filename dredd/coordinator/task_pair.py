from mem_store.init_status_item import InitStatusItem

class TaskPair(object):
    # Represntation of a task and its message components
    def __init__(self, message, task):
        self.message = message
        self.task = task
        self.init_status = self._new_init_status(
                            task.account_id,
                            message.parsed_message()['type'],
                            task.id_)

    def _new_init_status(self, account_id, message_type, task_id):
        return InitStatusItem(
                account_id,
                message_type,
                task_id)
