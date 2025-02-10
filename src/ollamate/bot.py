import json
import uuid

import ollama
from ollama import ChatResponse

from ollamate.settings import CHAT_HISTORY_PATH


class Bot:
    def __init__(
        self,
        host='http://localhost:11434', 
        model_name='llama3.2:3b',
        headers=dict(), 
        save_dir=CHAT_HISTORY_PATH
    ):
        self.client = ollama.Client(host=host, headers=headers)
        self.save_dir = save_dir
        self.chat_id = str(uuid.uuid4())
        self.model_name = model_name
        self.messages = []

    def config(self, model_name=None, host=None, headers=dict()):
        try:
            if host:
                self.client = ollama.Client(host=host, headers=headers) 
            if model_name:
                self.model_name = model_name
        except Exception as e:
            print(e)

    def save_chat(self):
        self.save_dir.mkdir(exist_ok=True)
        with open(self.save_dir / self.chat_id, 'w') as json_file:
            json.dump({
                "chat_id": self.chat_id,
                "model_name": self.model_name,
                "messages": self.messages
            }, json_file, indent=4, sort_keys=True)

    def create_new_chat(self):
        self.chat_id = str(uuid.uuid4())
        self.messages.clear()

    def chat(self, message, stream=True) -> ChatResponse:
        message = {'role': 'user', 'content': message}
        self.messages.append(message)

        return self.client.chat(
            model=self.model_name,
            messages=self.messages,
            stream=stream,
        )
