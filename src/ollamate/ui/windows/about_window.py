import tkinter as tk
from tkinter import scrolledtext
from tkinter.constants import END


class AboutWindow(tk.Toplevel):
    def __init__(self, master, title=None, info=None, hight=200, width=200):
        super().__init__(master)
        self.title(title if title else "Window")
        self.minsize(width, hight)

        name = info.get('name')
        version = info.get('version')
        summary = info.get('summary')
        license = info.get('license')
        homepage = info.get('urls').get('homepage')
        issues = info.get('urls').get('issues')
        authors = "\n".join([f"- {author}" for author in info.get('authors')])

        about_content = (
            f"🤖 {name} {version}\n\n"
            f"{summary}\n\n"
            f"License: the {license} license\n\n"
            f"Homepage: {homepage}\n"
            f"Issues: {issues}\n\n"
            f"☕ Developers:\n"
            f"==============\n"
            f"{authors}"
        )

        self.about = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.about.insert(END, about_content)
        self.about.config(state='disabled')
        self.about.pack(side='top', fill='both', expand=True)