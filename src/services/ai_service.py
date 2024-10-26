from abc import ABC, abstractmethod
# import openai
import requests
import json

class AIService(ABC):
    @abstractmethod
    async def get_response(self, message: str) -> str:
        pass

from zhipuai import ZhipuAI

class ZhipuAIService(AIService):
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
    
    async def get_response(self, message: str) -> str:
        try:
            # Remove await since ZhipuAI client is synchronous
            response = self.client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {"role": "system", "content": "你是一个友好的桌面宠物。请保持回答简短友好，主要提醒用户多喝水、适当休息和运动。"},
                    {"role": "user", "content": message}
                ],
                max_tokens=30
            )
            # Access the response content correctly
            return response.choices[0].message.content
        except Exception as e:
            print(f"ZhipuAI API error: {e}")
            return "抱歉，我现在连接不上我的大脑。"

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
