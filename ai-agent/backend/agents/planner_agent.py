from tools.task_db_tool import TaskDBTool
from tools.google_calendar_tool import GoogleCalendarTool

class PlannerAgent:
    def __init__(self):
        self.task_tool = TaskDBTool()
        self.calendar_tool = GoogleCalendarTool()

    def execute(self, intent):
        """
        Executes the action based on the simplified intent.
        """
        action = intent.get('action')
        params = intent.get('parameters', {})
        
        result = {"status": "error", "message": "Unknown action"}

        if action == 'create_task':
            result = self.task_tool.add_task(
                title=params.get('title', 'Untitled Task'),
                description=params.get('description'),
                due_date=params.get('due_date'),
                priority=params.get('priority', 'medium')
            )
        
        elif action == 'schedule_event':
            # Default to 1 hour duration if not specified
            start_time = params.get('start_time')
            if not start_time:
                # If LLM didn't extract time, fail gracefully or ask (here we fail)
                return {"status": "error", "message": "Missing start time for event"}
                
            # Naive end time calculation if missing (would be better in tool or helper)
            end_time = params.get('end_time')
            if not end_time:
                from datetime import datetime, timedelta
                try:
                    st = datetime.fromisoformat(start_time)
                    et = st + timedelta(hours=1)
                    end_time = et.isoformat()
                except:
                    pass

            # Check Availability with Scheduler Agent
            from agents.scheduler_agent import SchedulerAgent
            scheduler = SchedulerAgent()
            is_free = scheduler.calendar_tool.check_availability(start_time, end_time)
            
            if not is_free:
                # Try to reschedule/find new slot (Simple Auto-Rescheduling)
                new_start, new_end = scheduler.find_best_slot(duration_hours=1, start_date=start_time)
                if new_start:
                    return {
                        "status": "conflict", 
                        "message": f"Time slot conflict. Suggesting alternative: {new_start.isoformat()}",
                        "suggested_time": new_start.isoformat()
                    }
                else:
                    return {"status": "error", "message": "Time slot conflict and no alternative found."}

            result = self.calendar_tool.create_event(
                title=params.get('title', 'Untitled Event'),
                start_time=start_time,
                end_time=end_time,
                description=params.get('description'),
                location=params.get('location')
            )

        elif action == 'query':
            # Handle queries (list tasks, list events)
            pass
            
        elif action == 'notification':
             from agents.notification_agent import NotificationAgent
             notifier = NotificationAgent()
             notifier.send_notification(user_id=1, message=params.get('message', 'Alert'), channel=params.get('channel', 'email'))
             result = {"status": "success", "message": "Notification sent"}

        elif action == 'plan_week':
            from datetime import datetime, timedelta
            # Generate a few items
            now = datetime.now()
            
            # 1. Strategy Session
            self.calendar_tool.create_event("Strategy Session", (now + timedelta(days=1, hours=10)).isoformat(), (now + timedelta(days=1, hours=11)).isoformat(), "Weekly strategy alignment")
            
            # 2. Focus Time
            self.calendar_tool.create_event("Deep Work", (now + timedelta(days=1, hours=14)).isoformat(), (now + timedelta(days=1, hours=16)).isoformat(), "Coding block")
            
            # 3. Task
            self.task_tool.add_task("Review Metrics", "Check weekly KPIs", priority="high")
            
            result = {"status": "success", "message": "Week planned with 2 events and 1 task."}

        elif action == 'chat':
            result = {"status": "success", "message": params.get('response', "Hello!")}

        return result
