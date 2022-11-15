from tasks import ResultTask


class GenLog:
    def __init__(self, tasks_log_path: str, profiles_log_path: str) -> None:
        self.tasks_log_path = tasks_log_path
        self.profiles_log_path = profiles_log_path

    def log_task(self, task: ResultTask):
        message = f'{task.status} | {task.id} | {task.task_type} | {task.value} | {task.profile_name}' + '\n'
        
        with open(self.tasks_log_path, 'a') as log:
            log.write(message)
            


if __name__ == '__main__':
    pass
