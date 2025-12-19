from database.models import Task, db
from datetime import datetime

class TaskDBTool:
    def add_task(self, title, description=None, due_date=None, priority='medium'):
        """Adds a new task to the database."""
        try:
            # Simple date parsing or assume it's passed as a datetime object or ISO string in real usage
            # For now, let's assume due_date is None or a string
            parsed_date = None
            if due_date:
                # Naive parsing, improve strictly for agent usage
                try:
                    parsed_date = datetime.fromisoformat(due_date)
                except:
                    pass 

            task = Task(title=title, description=description, due_date=parsed_date, priority=priority)
            db.session.add(task)
            db.session.commit()
            return {"status": "success", "task": task.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_tasks(self, status=None):
        """Lists tasks, optionally filtering by status."""
        query = Task.query
        if status:
            query = query.filter_by(status=status)
        tasks = query.all()
        return [t.to_dict() for t in tasks]

    def update_task_status(self, task_id, status):
        """Updates the status of a task."""
        task = Task.query.get(task_id)
        if task:
            task.status = status
            db.session.commit()
            return {"status": "success", "task": task.to_dict()}
        return {"status": "error", "message": "Task not found"}
