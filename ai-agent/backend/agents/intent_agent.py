import json
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import Config

class IntentAgent:
    def __init__(self):
        self.google_api_key = Config.GOOGLE_API_KEY
        self.openai_api_key = Config.OPENAI_API_KEY
        
        if self.google_api_key:
             self.llm = ChatGoogleGenerativeAI(google_api_key=self.google_api_key, model=Config.MODEL_NAME, temperature=0)
        elif self.openai_api_key:
            self.llm = ChatOpenAI(api_key=self.openai_api_key, model=Config.MODEL_NAME, temperature=0)
        else:
            self.llm = None

    def parse_intent(self, user_input):
        """
        Analyzes user input and returns a structured JSON intent.
        """
        # 1. Quick Local Check for Greetings (Fast & Cheap)
        # This works regardless of LLM status
        lower_input = user_input.lower()
        if any(word in lower_input.split() for word in ["hi", "hello", "hey", "hola", "greetings"]):
             return {
                "action": "chat",
                "parameters": {
                    "response": "Hello! I am your AI personal assistant. How can I help you manage your tasks today?"
                },
                "confidence": 1.0
             }

        if not self.llm:
            # Fallback for demo without API key
            return self._mock_intent(user_input)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an advanced intent recognition agent. "
                       "Your ONLY job is to output a single valid JSON object. Do not output markdown, explanations, or code blocks. "
                       "Analyze the user's input and extract: \n"
                       "- 'action': One of [create_task, schedule_event, query, chat, plan_week, notification]\n"
                       "- 'parameters': A dictionary of relevant details (title, date, priority, response, channel)\n"
                       "- 'confidence': A float between 0 and 1\n\n"
                       "Examples:\n"
                       "Input: 'Buy milk'\nOutput: {{\"action\": \"create_task\", \"parameters\": {{\"title\": \"Buy milk\", \"priority\": \"medium\"}}, \"confidence\": 0.9}}\n"
                       "Input: 'Hi there'\nOutput: {{\"action\": \"chat\", \"parameters\": {{\"response\": \"Hello! How can I help?\"}}, \"confidence\": 1.0}}"),
            ("user", "{input}")
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        
        try:
            return chain.invoke({"input": user_input})
        except Exception as e:
            print(f"LLM Error: {e}. Falling back to rule-based engine.")
            return self._mock_intent(user_input)

    def _mock_intent(self, user_input):
        # Simple keyword matching for demo purposes
        user_input = user_input.lower()
        if "remind me" in user_input or "task" in user_input:
            return {
                "action": "create_task",
                "parameters": {
                    "title": user_input,
                    "priority": "medium"
                },
                "confidence": 0.9
            }
        elif "schedule" in user_input or "meeting" in user_input:
            return {
                "action": "schedule_event",
                "parameters": {
                    "title": user_input,
                    "start_time": "2025-12-20T10:00:00" # Placeholder
                },
                "confidence": 0.9
            }
        elif "email" in user_input or "send" in user_input:
             return {
                "action": "notification",
                "parameters": {
                    "message": user_input,
                    "channel": "email"
                },
                "confidence": 0.8
             }
        elif "plan" in user_input:
             return {
                "action": "plan_week",
                "parameters": {},
                "confidence": 0.9
             }
        # Casual Conversation / Greetings
        elif any(word in user_input for word in ["hi", "hello", "hey", "hola", "greetings"]):
             return {
                "action": "chat",
                "parameters": {
                    "response": "Hello! I'm ready to help you organize your tasks and schedule. Try saying 'Plan my week' or 'Add a task'."
                },
                "confidence": 1.0
             }
        return {"action": "unknown", "parameters": {}, "confidence": 0}
