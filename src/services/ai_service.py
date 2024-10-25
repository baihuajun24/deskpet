from abc import ABC, abstractmethod
# import openai
import requests
import json

class AIService(ABC):
    @abstractmethod
    async def get_response(self, message: str) -> str:
        pass

class OpenAIService(AIService):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def get_response(self, message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful desktop pet. Keep responses concise and friendly."},
                    {"role": "user", "content": message}
                ],
                max_tokens=100  # Keep responses short
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now."

class OllamaService(AIService):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    async def get_response(self, message: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "llama2",  # or whatever model you're using
                    "prompt": message,
                    "system": "You are a helpful desktop pet. Keep responses concise and friendly."
                }
            )
            return response.json()['response']
        except Exception as e:
            print(f"Ollama API error: {e}")
            return "Sorry, I'm having trouble connecting to my local brain."