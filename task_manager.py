from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_title):
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_task(self, task_title):
        for task in self.tasks:
            if task.title == task_title:
                return task
        return None

    def list_tasks(self):
        for task in self.tasks:
            print(task)

    def list_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def list_overdue_tasks(self):
        return [task for task in self.tasks if task.is_due() and task.status != "Completed"]

    def update_task_status(self, task_title, new_status):
        task = self.get_task(task_title)
        if task:
            task.status = new_status