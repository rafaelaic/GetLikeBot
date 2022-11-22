from getlike import *

class GenLog:
    def __init__(self, tasks_log_path: str, profiles_log_path: str) -> None:
        self.tasks_log_path = tasks_log_path
        self.profiles_log_path = profiles_log_path

    def log_profile(self, result :ResultProfile):
        message = '\n+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n' + \
            f'{result.id} | {result.earned:.2f} RUB' + '\n' \
            + f'Success: {result.success_tasks} | Hided: {result.hided_tasks}' + '\n+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=\n'
        
        print(message)
        with open(self.profiles_log_path, 'a') as log:
            log.write(message)
    
    def log_task(self, task: ResultTask):
        message = f'{task.status} | {task.id} | {task.task_type} | {task.value} | {task.profile_name}' + '\n'
        
        print(message)
        with open(self.tasks_log_path, 'a') as log:
            log.write(message)
            
    def log_message(self, message :str):
        print(message)

if __name__ == '__main__':
    pass
