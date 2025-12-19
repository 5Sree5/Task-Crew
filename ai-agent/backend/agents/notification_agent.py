class NotificationAgent:
    def send_notification(self, user_id, message, channel='email'):
        """
        Sends a notification. 
        In a real app, this would connect to SendGrid, Twilio, or Firebase.
        """
        print(f"[NOTIFICATION - {channel}] To User {user_id}: {message}")
        return True

    def schedule_reminder(self, task_id, time):
        # Integration with APScheduler would go here
        print(f"[REMINDER SCHEDULED] Task {task_id} at {time}")
        return True
