import tkinter as tk


RELIEF = 'groove'

padx, pady = (3, 10)
ipadx, ipady = (30, 20)

class MessageBoxFrame(tk.Frame):
    def __init__(self, master, callback=None):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        self.callback = callback

        self.message_entry = tk.Text(self, height=1) 
        self.message_entry.pack(
            side='left', fill='both', expand=True,
            ipadx=ipadx, ipady=ipady,padx=padx, pady=pady
        )
        self.message_entry.config(relief=RELIEF)

        self.send_button = tk.Button(self, text='Send', command=self.callback)
        self.send_button.pack(side='left', ipadx=ipadx, ipady=ipady)
        self.send_button.config(relief=RELIEF)

        self.message_entry.insert(tk.END, "Write here")
        self.message_entry.bind('<Key-Return>', self.callback)