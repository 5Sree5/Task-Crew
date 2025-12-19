from tools.google_calendar_tool import GoogleCalendarTool
from datetime import datetime, timedelta

class SchedulerAgent:
    def __init__(self):
        self.calendar_tool = GoogleCalendarTool()

    def find_best_slot(self, duration_hours=1, start_date=None):
        """
        Finds the next available slot.
        This is a simplified logic: checks hourly slots starting from start_date/now.
        """
        if not start_date:
            start_date = datetime.now()
        else:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)

        # Check next 10 slots
        for i in range(10):
            slot_start = start_date + timedelta(hours=i)
            slot_end = slot_start + timedelta(hours=duration_hours)
            
            # Simple check using the tool's check_availability
            is_free = self.calendar_tool.check_availability(slot_start.isoformat(), slot_end.isoformat())
            
            if is_free:
                return slot_start, slot_end
                
        return None, None

    def reschedule_conflict(self, event_id, new_time):
        # Placeholder for intelligent rescheduling logic
        pass
