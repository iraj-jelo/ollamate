import tkinter as tk
from tkinter import messagebox


padx, pady = (0, 5), (5, 5)
field_padx, field_pady = (0, 3)

class ModelsWindow(tk.Toplevel):
    def __init__(
        self, master, title="Models", hight=200, width=300, 
        settings=None, callback=None, setting_variable='ollama_models'):
        super().__init__(master)
        self.root = master
        self.title(title)
        self.settings = settings
        self.setting_variable = setting_variable
        self.callback = callback

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side='top', fill='both', expand=True, anchor='n', padx=(5, 5), pady=pady)

        self.entry_frame = tk.Frame(self.top_frame)
        self.entry_frame.pack(side='top', fill='x', pady=(0, 5))

        self.label = tk.Label(self.entry_frame, text="Model name")
        self.label.pack(side='left')

        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side='left', fill='both', expand=True)

        self.add_button = tk.Button(self.entry_frame, text="Add", command=self.add_item)
        self.add_button.pack(side='right')

        self.listbox = tk.Listbox(self.top_frame)
        self.listbox.pack(side='bottom', fill='both', expand=True)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side='bottom', fill='x')

        self.select_button = tk.Button(self.buttons_frame, text="Select", command=self.get_selected_item)
        self.select_button.pack(side='right', padx=padx, pady=pady)

        self.remove_button = tk.Button(self.buttons_frame, text="Remove", command=self.remove_item)
        self.remove_button.pack(side='right', padx=padx, pady=pady)

        self.close_button = tk.Button(self.buttons_frame, text="Close", command=self.destroy)
        self.close_button.pack(side='right', padx=padx, pady=pady)

        self._load_data()

    def _load_data(self):
        models = self.settings.config[self.setting_variable]
        for model in models:
            self.listbox.insert(tk.END, model) 

    def _save_data(self):
        self.settings.config[self.setting_variable] = self.listbox.get(0, tk.END)
        self.settings.save()
        if self.callback:
            self.callback(settings=self.settings)

    def add_item(self):
        item = self.entry.get()
        if item:
            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END) # Clear the entry field
            self._save_data()
        else:
            messagebox.showwarning("Warning", "Please enter an item.")

    def remove_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_index)
            self._save_data()
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item to remove.")

    def get_selected_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_item = self.listbox.get(selected_index)
            messagebox.showinfo("Selected Item", f"You selected: {selected_item}")
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item.")

