import argparse
from enum import StrEnum

from ollamate.settings import Settings
from ollamate.bot import Bot

from ollamate.settings import APP_ICON, PROJECT_NAME


VERSION = "v0.0.1"

PROJECT_INFO = {
    "name": PROJECT_NAME.capitalize(),
    "version": VERSION,
    "summary": f"{PROJECT_NAME.capitalize()} is a simple AI assistant for local LLMs hosted on your machine using Ollama. it will support some custom functions and a RAG system.",
    "license": "MIT",
    "authors": ["Iraj Jelodari <Iraj.Jelo@gmail.com>",],
    "urls": {
        "homepage": f"https://github.com/iraj-jelo/{PROJECT_NAME}",
        "issues": f"https://github.com/iraj-jelo/{PROJECT_NAME}/issues"
    },
}

class Interface(StrEnum):
    TK = 'tk'


def tk_app(app_info=None, bot=None, settings=None):
    import tkinter as tk
    from .ui.app import ChatApp 

    root = tk.Tk()
    app = ChatApp(root, app_info=app_info, settings=settings, bot=bot)
    app.ICON = tk.PhotoImage(file=APP_ICON)

    # Set minsize to avoid reducing widgets in pack list 
    root.minsize(width=900, height=440)
    root.iconphoto(True, app.ICON)
    root.geometry('1100x440+300+300')
    root.mainloop()

def main():
    project_name = PROJECT_INFO.get('name')
    version = PROJECT_INFO.get('version')

    parser = argparse.ArgumentParser(prog=project_name, description=project_name)
    parser.add_argument(
        "-v", "--version", help="Print the app version.",
        action='version', version=f"%(prog)s {version}")
    parser.add_argument(
        "-i", "--gui", default=Interface.TK,
        help="Use a certain GUI to interact with the app.", )

    args = parser.parse_args()

    settings = Settings()
    bot = Bot()

    if args.gui == Interface.TK:
        tk_app(app_info=PROJECT_INFO, bot=bot, settings=settings)


if __name__ == "__main__":
    main()