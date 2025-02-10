import tkinter as tk
from tkinter import font
from tkinter import scrolledtext

from .message_box import MessageBoxFrame


USER_TAG = "user"
AI_TAG = "ai"

class ChatFrame(tk.Frame):
    def __init__(self, master, send_callback=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        pw = tk.PanedWindow(self, orient='vertical', showhandle=False)

        self.chat_box = scrolledtext.ScrolledText(pw, wrap=tk.WORD, state='disabled')
        self.message_box = MessageBoxFrame(pw, callback=send_callback)

        pw.add(self.chat_box, stretch='always', minsize=300)
        pw.add(self.message_box, stretch='never', minsize=100)

        pw.pack(fill='both', expand=True)

        self.chat_box.tag_configure(
            USER_TAG, selectbackground='yellow',
            foreground='blue', background='#f1f1f1',)
        self.chat_box.tag_configure(AI_TAG, foreground='black')

        self.set_chat_box_font()

    def set_chat_box_font(self, family='Times', size=13, weight='normal'):
        self.chat_box.config(font=font.Font(family=family, size=size, weight=weight))

    def clear_message_box(self):
        self.message_box.message_entry.delete(1.0, tk.END)

    def enable_message_box(self):
        self.message_box.message_entry.configure(state='normal')

    def disable_message_box(self):
        self.message_box.message_entry.configure(state='disabled')

    def clear_chat_box(self):
        self.chat_box.config(state='normal')
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.config(state='disabled')

    def print_message(self, role=None, message=None, stream=False):
        contact = 'You' if (role == USER_TAG) else "Assistant"
        message = message if stream else f"{contact}: {message}\n"
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, message, role)
        self.chat_box.config(state='disabled')
        self.chat_box.yview(tk.END)
