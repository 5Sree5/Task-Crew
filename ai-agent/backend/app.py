import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from database.db import db
from database.models import Task, Event, User
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Extensions
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    # Register Blueprints / Routes
    @app.route('/', methods=['GET'])
    def index():
        return "AI Agent Backend is Running! Use /api/ endpoints."

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "ai-agent-backend"})

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        data = request.json
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            # Date handling needed here later
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201

    @app.route('/api/calendar/events', methods=['GET'])
    def get_events():
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events])

    # AI CHAT ENDPOINT
    @app.route('/api/chat', methods=['POST'])
    def chat():
        from agents.intent_agent import IntentAgent
        from agents.planner_agent import PlannerAgent
        
        data = request.json
        user_message = data.get('message', '')
        
        intent_agent = IntentAgent()
        planner_agent = PlannerAgent()
        
        # 1. Understand Intent
        intent = intent_agent.parse_intent(user_message)
        
        # 2. Execute Plan
        execution_result = planner_agent.execute(intent)
        
        # 3. Formulate Response
        if intent.get('action') == 'chat':
             response_text = execution_result.get('message')
        else:
             response_text = f"I've processed your request: {intent.get('action')}. Result: {execution_result.get('status')}"
        
        return jsonify({
            "response": response_text,
            "intent": intent,
            "execution": execution_result
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
