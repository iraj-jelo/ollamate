import json
from pathlib import Path


BASE_PATH = Path(__file__).parent

PROJECT_NAME = BASE_PATH.stem.replace("_", " ")

APP_ICON = BASE_PATH / "img/ollama.png"

CONFIG_PATH = BASE_PATH / 'settings.json'

CHAT_HISTORY_PATH = BASE_PATH / 'chats/'

class Settings:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config = None
        self.load()

    def load(self):
        try:
            with open(self.config_path) as file:
                self.config = json.load(file)
        except FileNotFoundError:
            print(f"Config file '{self.config_path}' not found. Using default settings.")

    def save(self):
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file, indent=4, sort_keys=True)
