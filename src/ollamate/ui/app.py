import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import json

from .widgets.chat_box import ChatFrame
from .windows.about_window import AboutWindow
from .windows.history_window import HistoryWindow
from .windows.settings_window import SettingsWindow
from .windows.models_window import ModelsWindow

from ..utils import set_proxy


USER_TAG = "user"
AI_TAG = "ai"

class ChatApp(tk.Widget):
    def __init__(self, root, app_info=None, settings=None, bot=None):
        self.root = root
        self.settings = settings
        self.bot = bot
        self.app_info = app_info

        self.root.title(self.app_info.get('name').capitalize())
        
        if not self.settings:
            print("ُThere is no settings file.")

        self.config_app()

        # Frames:
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side="top", expand=True, fill="both")

        # Widgets:
        
        self.chat_frame = ChatFrame(self.main_frame, send_callback=self.send_message)
        self.chat_frame.pack(side='right')

        # Menu bar

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.chats_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.chats_menu.add_command(label="New Chat", command=self.create_new_chat)
        self.chats_menu.add_command(label="History", command=self.open_history)
        self.chats_menu.add_command(label="Close", command=self.root.destroy)
        self.settings_menu.add_command(label="Settings", command=self.open_settings)
        self.settings_menu.add_command(label="Ollama Models", command=self.open_models_window)
        self.about_menu.add_command(label="About", command=self.open_about)

        self.menu_bar.add_cascade(label="Chats", menu=self.chats_menu)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

    def send_message(self, event=None):
        message = self.chat_frame.message_box.message_entry.get("1.0", "end-1c")
        if message:
            self.chat_frame.print_message(role=USER_TAG, message=message)
            self.stream_ai_response(message)

    def stream_ai_response(self, user_message):
        threading.Thread(target=self.get_ai_response, args=(user_message,)).start()

    def get_ai_response(self, user_message):
        response = ""
        self.chat_frame.enable_message_box()
        self.chat_frame.clear_message_box()
        self.chat_frame.disable_message_box()
        self.chat_frame.print_message(role=AI_TAG, message="Assistant: ", stream=True)
        try:
            for chunk in self.bot.chat(user_message):
                response += chunk.message.content
                data = json.loads(chunk.json())
                created_at = data.get("created_at")
                role = data.get("message").get("role")
                self.chat_frame.print_message(role=AI_TAG, message=chunk.message.content, stream=True)

            self.chat_frame.print_message(role=AI_TAG, message="\n", stream=True)
            self.bot.messages.append({"role": role, "content": response, "created_at": created_at})
            self.bot.save_chat()
            self.chat_frame.enable_message_box()
        except Exception as e:
            error_message = f"Failed to get response from AI: {str(e)}"
            messagebox.showerror("Error", error_message)
            self.chat_frame.print_message(role=AI_TAG, message=f"{error_message}\n", stream=True)
            self.chat_frame.enable_message_box()

    def config_app(
        self,
        ollama_host=None,
        model_name=None,
        http_proxy="", 
        https_proxy="",
        socks5_proxy=""
    ):
        ollama_host = self.settings.config.get("ollama_host", ollama_host)
        model_name = self.settings.config.get("ollama_selected_model_name", model_name)
        http_proxy = self.settings.config.get("http_proxy", http_proxy)
        https_proxy = self.settings.config.get("https_proxy", https_proxy) 
        socks5_proxy = self.settings.config.get("socks5_proxy", socks5_proxy)

        # @TODO: set options in settings window to config the chat font
        # self.chat_frame.set_chat_box_font(family=, size=, weight=)

        if http_proxy or https_proxy or socks5_proxy:
            set_proxy(http=http_proxy, https=https_proxy, socks5=socks5_proxy)

        if model_name or ollama_host:
            bot_parameters = {"model_name": model_name, "host": ollama_host}
            self.bot.config(**bot_parameters)
 
    def save_settings(self, window=None, settings=None):
        try:
            self.config_app()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get response from AI: {str(e)}")
        if window:
            window.destroy()

    def load_chat(self, messages=None, chat_id=None):
        self.bot.messages = messages
        self.bot.chat_id = chat_id
        self.chat_frame.clear_chat_box()
        for message in messages:
            role = message.get('role')
            content = message.get('content')
            self.chat_frame.print_message(role=role, message=content)

    def create_new_chat(self):
        self.bot.create_new_chat()
        self.chat_frame.clear_chat_box()

    def open_history(self):
        _window = self.open_window(HistoryWindow(self.root, loading_callback=self.load_chat))

    def open_settings(self):
        _window = self.open_window(SettingsWindow(self.root, settings=self.settings, callback=self.save_settings))

    def open_models_window(self):
        _window = self.open_window(ModelsWindow(self.root, settings=self.settings, callback=self.save_settings, setting_variable='ollama_models'))

    def open_about(self):
        _window = self.open_window(AboutWindow(self.root, title="About", info=self.app_info), geometry=('500x300+600+300'))

    def open_window(self, window, geometry=('+600+300')):
        window.geometry(geometry)
        return window
