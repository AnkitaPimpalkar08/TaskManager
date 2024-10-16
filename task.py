from datetime import datetime

class Task:
    def __init__(self, title, description, due_date, priority="Low", status="Pending"):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.priority = priority
        self.status = status
    
    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date.strftime('%Y-%m-%d')}\nPriority: {self.priority}\nStatus: {self.status}"

    def mark_completed(self):
        self.status = "Completed"

    def is_due(self):
        return self.due_date < datetime.now()