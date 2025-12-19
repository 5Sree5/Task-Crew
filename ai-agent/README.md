# AI Personal Task Automation Agent

A premium, production-ready AI agent that automates tasks and schedule management using a local Python backend and a React/TypeScript frontend.

## Features

- **Natural Language Intent**: "Schedule a meeting with John tomorrow" -> Automatically creates a calendar event.
- **Task Management**: Drag-and-drop board (UI ready, list view implemented) with priority tracking.
- **Calendar Sync**: Real-time view of your schedule.
- **Simulated Google/Notion Tools**: Works locally without needing immediate API keys (uses local SQL DB).
- **Premium UI**: Dark mode, Framer Motion animations, ShadCN-inspired design.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## Setup & Run

### 1. Backend

Navigate to the `backend` folder:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r ../requirements.txt
```

Initialize and Seed Database:
```bash
python database/seed.py
```

Run Screen:
```bash
python app.py
```
Server will run at `http://localhost:5000`.

### 2. Frontend

Open a new terminal and navigate to the `frontend` folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the Development Server:
```bash
npm run dev
```
App will open at `http://localhost:5173`.

## Usage

1. Open the dashboard.
2. Type in the **AI Assistant** chat panel on the right.
3. Try: "Remind me to call Mom tomorrow" or "Schedule a team meeting at 2pm".
4. Watch the Task Board or Schedule update automatically (refresh/polling is enabled).

## Architecture

- **Backend**: Flask + SQLAlchemy (SQLite) + LangChain (Agents).
- **Frontend**: React + Vite + TailwindCSS + Lucide Icons.
- **AI Agents**:
    - `IntentAgent`: Parses text into structural JSON.
    - `PlannerAgent`: Calls the appropriate tool (`TaskDBTool` or `GoogleCalendarTool`).

## Configuration

Edit `backend/config.py` to add real OpenAI API keys.
If no key is present, the system runs in **Demo Mode** with mock responses.

```python
# backend/config.py
OPENAI_API_KEY = "your-key-here"
```
