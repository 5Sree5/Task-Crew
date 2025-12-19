@echo off
echo Starting AI Agent System...

start cmd /k "cd ai-agent/backend && python app.py"
start cmd /k "cd ai-agent/frontend && npm run dev"

echo System started. Backend: Port 5000, Frontend: Port 5173.
