import json
from datetime import datetime as dt
import tkinter as tk

from ollamate.settings import CHAT_HISTORY_PATH


padx, pady = (0, 5), (5, 5)
field_padx, field_pady = (0, 3)

class HistoryWindow(tk.Toplevel):
    def __init__(
        self, master, title="Chat History", hight=200, width=500,
        settings=None, loading_callback=None):
        super().__init__(master)
        self.title(title)
        self.settings = settings
        self.minsize(width, hight)
        self.loading_callback = loading_callback
        self.history_path = CHAT_HISTORY_PATH

        self.focus_force()
        self.grab_set()

        self.main_frame = tk.Frame(self)
        self.create_history_frame(self.main_frame)
        self.create_buttons_frame(self.main_frame)
        self.main_frame.pack(side='left', fill='both', expand=True)

        self.load_history()

    def create_buttons_frame(self, frame):
        self.buttons_frame = tk.Frame(frame)
        self.buttons_frame.pack(side='bottom', fill='x', anchor='s')

        self.select_button = tk.Button(self.buttons_frame, text="Load", command=self.load_item)
        self.select_button.pack(side=tk.RIGHT, padx=padx, pady=pady)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_item)
        self.delete_button.pack(side=tk.RIGHT, padx=padx, pady=pady)

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=padx, pady=pady)

    def load_history(self):
        if self.history_path.exists():
            _dir, _, files = next(self.history_path.walk())
            history = [json.loads((self.history_path / f).read_text()) for f in files]

            history = sorted(history, key=lambda data: -dt.fromisoformat(data['messages'][-1]['created_at']).timestamp())
            for chat in history:
                chat_id = chat.get('chat_id')
                first_message = chat.get('messages')[0].get('content')
                last_message = chat.get('messages')[-1].get('created_at')
                last_message = dt.fromisoformat(last_message).strftime("%Y-%m-%d [%H:%M:%S]")
                self.history_treeview.insert("", 'end', text ="L1", values =(first_message, last_message, chat_id))

    def create_history_frame(self, frame):
        self.history_frame = tk.Frame(frame)
        self.history_treeview = tk.ttk.Treeview(self.history_frame, selectmode='browse')

        self.history_treeview["columns"] = ("1", "2")
        self.history_treeview['show'] = 'headings'

        self.history_treeview.column("1", width =90, anchor ='w')
        self.history_treeview.column("2", width =10, anchor ='e')

        self.history_treeview.heading("1", text ="Chat")
        self.history_treeview.heading("2", text ="Time")

        self.vertical_scrollbar = tk.ttk.Scrollbar(
            self.history_frame,
            orient ="vertical",
            command=self.history_treeview.yview
        )
        self.history_treeview.configure(xscrollcommand =self.vertical_scrollbar.set)
        self.history_treeview.pack(side ='left', fill='both', expand=True)
        self.vertical_scrollbar.pack(side ='right', fill ='y')
        self.history_frame.pack(side='top', fill='both', expand=True, padx=padx, pady=pady)

    def select_item(self):
        index = next(iter(self.history_treeview.selection()))
        item = self.history_treeview.item(index)
        chat_id = item['values'][2] # chat_id
        if chat_id:
            return index, json.loads((self.history_path / chat_id).read_text())

    def load_item(self):
        index, chat = self.select_item() 
        if chat:
            self.loading_callback(messages=chat['messages'], chat_id=chat["chat_id"])

    def delete_item(self):
        index, chat = self.select_item()
        chat = self.history_path / chat['chat_id']
        if chat.exists():
            chat.unlink()
            self.history_treeview.delete(index)
