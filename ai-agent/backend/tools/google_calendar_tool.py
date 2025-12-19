from database.models import Event, db
from datetime import datetime

class GoogleCalendarTool:
    """
    A tool that simulates interaction with Google Calendar by using a local SQL table.
    In a real deployment, this would use the Google Calendar API.
    """
    
    def create_event(self, title, start_time, end_time, description=None, location=None):
        """
        Creates a calendar event.
        start_time and end_time should be ISO format strings.
        """
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            
            event = Event(
                title=title,
                start_time=start,
                end_time=end,
                description=description,
                location=location
            )
            db.session.add(event)
            db.session.commit()
            return {"status": "success", "event": event.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_events(self, start_range=None, end_range=None):
        """
        Lists events. Date range filtering can be added here.
        """
        events = Event.query.all()
        # In a real app we'd filter by date range
        return [e.to_dict() for e in events]

    def check_availability(self, start_time, end_time):
        """
        Checks if a time slot is free. 
        Simple overlap check.
        """
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        
        # Check for overlaps
        # (StartA <= EndB) and (EndA >= StartB)
        overlap = Event.query.filter(Event.start_time < end, Event.end_time > start).first()
        if overlap:
            return False
        return True
