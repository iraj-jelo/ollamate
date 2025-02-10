import tkinter as tk


padx, pady = (0, 5), (5, 5)
field_padx, field_pady = (0, 3)

class SettingsWindow(tk.Toplevel):
    def __init__(
        self, master, title="Settings", hight=200, width=300,
        settings=None, callback=None):
        super().__init__(master)
        self.title(title)
        self.settings = settings
        self.minsize(width, hight)
        self.callback = callback

        self.label_width = 20

        self.focus_force()
        # Forces tkinter to focus on a single window, and does not allow this focus to shift, until the window has been destroyed.
        # self.grab_set()

        self.create_ollama_frame()
        self.create_proxy_frame()

        self.load_settings()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side='bottom', fill='x', expand=True, anchor='s')

        self.save_button = tk.Button(self.buttons_frame, text="Save", command=self.save_settings)
        self.save_button.pack(side=tk.RIGHT, padx=padx, pady=pady)

        self.cancel_button = tk.Button(self.buttons_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=padx, pady=pady)

    def create_ollama_frame(self):
        # Frames:

        self.ollama_frame = tk.LabelFrame(self, text="Ollama")
        self.ollama_frame.pack(side='top', fill='both', anchor='center', padx=padx, pady=pady)

        self.ollama_labels_frame = tk.Frame(self.ollama_frame)
        self.ollama_labels_frame.pack(side='left', fill='both', anchor='center', padx=padx, pady=pady)

        self.ollama_fields_frame = tk.Frame(self.ollama_frame)
        self.ollama_fields_frame.pack(side='right', fill='both', expand=True, padx=padx, pady=pady)

        # Labels:

        self.ollama_model_label = tk.Label(self.ollama_labels_frame, text='Model'.ljust(self.label_width))
        self.ollama_model_label.pack(padx=field_padx, pady=field_pady)

        self.ollama_host_label = tk.Label(self.ollama_labels_frame, text='Host'.ljust(self.label_width))
        self.ollama_host_label.pack(padx=field_padx, pady=field_pady)

        # Fields:

        self.ollama_models_combobox = tk.ttk.Combobox(self.ollama_fields_frame)
        self.ollama_models_combobox['state'] = 'readonly'
        self.ollama_models_combobox.setting_variables = {'loading': 'ollama_models', 'saving': 'ollama_selected_model_name'}
        self.ollama_models_combobox.pack(fill='x', padx=field_padx, pady=field_pady)

        self.ollama_host_entry = tk.Entry(self.ollama_fields_frame)
        self.ollama_host_entry.setting_variables = {'loading': 'ollama_host', 'saving': 'ollama_host'}
        self.ollama_host_entry.pack(fill='x', padx=field_padx, pady=field_pady)


    def create_proxy_frame(self):
        # Frames:

        self.proxy_frame = tk.LabelFrame(self, text="Proxy")
        self.proxy_frame.pack(side='top', fill='both', anchor='center', padx=padx, pady=pady)

        self.proxy_labels_frame = tk.Frame(self.proxy_frame)
        self.proxy_labels_frame.pack(side='left', fill='both', anchor='center', padx=padx, pady=pady)

        self.proxy_fields_frame = tk.Frame(self.proxy_frame)
        self.proxy_fields_frame.pack(side='right', fill='both', expand=True, padx=padx, pady=pady)

        # Labels:

        self.http_proxy_label = tk.Label(self.proxy_labels_frame, text='HTTP Proxy'.ljust(self.label_width))
        self.http_proxy_label.pack(padx=field_padx, pady=field_pady)

        self.https_proxy_label = tk.Label(self.proxy_labels_frame, text='HTTPS Proxy'.ljust(self.label_width))
        self.https_proxy_label.pack(padx=field_padx, pady=field_pady)

        self.socks5_proxy_label = tk.Label(self.proxy_labels_frame, text='SOCKS5 Proxy'.ljust(self.label_width))
        self.socks5_proxy_label.pack(padx=field_padx, pady=field_pady)

        # Fields:

        self.http_proxy_entry = tk.Entry(self.proxy_fields_frame)
        self.http_proxy_entry.setting_variables = {'loading': 'http_proxy', 'saving': 'http_proxy'}
        self.http_proxy_entry.pack(fill='x', padx=field_padx, pady=field_pady)

        self.https_proxy_entry = tk.Entry(self.proxy_fields_frame)
        self.https_proxy_entry.setting_variables = {'loading': 'https_proxy', 'saving': 'https_proxy'}
        self.https_proxy_entry.pack(fill='x', padx=field_padx, pady=field_pady)

        self.socks5_proxy_entry = tk.Entry(self.proxy_fields_frame)
        self.socks5_proxy_entry.setting_variables = {'loading': 'socks5_proxy', 'saving': 'socks5_proxy'}
        self.socks5_proxy_entry.pack(fill='x', padx=field_padx, pady=field_pady)

    def get_fields(self):
        field_types = [tk.Entry, tk.ttk.Combobox]
        fields = [attr for attr_name in dir(self) if type(attr := getattr(self, attr_name)) in field_types]
        return fields

    def save_settings(self):
        for field in self.get_fields():
            saving_variable = field.setting_variables.get('saving')
 
            if isinstance(field, tk.Entry):
                self.settings.config[saving_variable] = field.get()

            if isinstance(field, tk.ttk.Combobox):
                # self.settings.config[saving_variable] = field.current()
                self.settings.config[saving_variable] = field.get()
        self.settings.save()
        self.callback(window=self, settings=self.settings) if self.callback else self.destroy()


    def load_settings(self):
        self.settings.load()
        for field in self.get_fields():
            loading_variable = field.setting_variables.get('loading')
            if isinstance(field, tk.Entry):
                field["textvariable"] = tk.StringVar(value=self.settings.config.get(loading_variable, ''))

            if isinstance(field, tk.ttk.Combobox):
                field['values'] = self.settings.config.get(loading_variable, [])

                current_value = self.settings.config.get(field.setting_variables.get('saving'), 0)
                current = field['values'].index(current_value) if current_value in field['values'] else -1
                if current >= 0:
                    field.current(current)
