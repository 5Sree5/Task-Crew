from app import create_app
from database.db import db
from database.models import Task, Event, User
from datetime import datetime, timedelta

def seed():
    app = create_app()
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()

        # Create User
        user = User(username='demo_user', email='user@demo.com')
        db.session.add(user)
        db.session.commit()

        # Create Tasks
        tasks = [
            Task(title='Review PR #42', description='Check the new authentication logic', status='todo', priority='high', user_id=user.id),
            Task(title='Update Documentation', description='Add API docs for the new endpoints', status='in-progress', priority='medium', user_id=user.id),
            Task(title='Team Sync', description='Weekly sync with engineering team', status='done', priority='low', user_id=user.id),
        ]
        
        # Create Events
        now = datetime.now()
        events = [
            Event(title='Sprint Planning', start_time=now + timedelta(days=1, hours=2), end_time=now + timedelta(days=1, hours=3), user_id=user.id, location='Room 101'),
            Event(title='Client Call', start_time=now + timedelta(days=2, hours=4), end_time=now + timedelta(days=2, hours=5), user_id=user.id, location='Zoom'),
        ]

        db.session.add_all(tasks)
        db.session.add_all(events)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
