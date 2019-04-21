#!/usr/bin/env python3
from tkinter import Tk, Frame, Text, Entry, Button, TOP, LEFT, RIGHT, BOTH, X

class TelnetCommunicator(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.wtext = Text(self, width=40, height=10)
        self.wentry, self.wsend = Entry(self), Button(self)
        self.wtext.pack(side=TOP, fill=BOTH, expand=1)
        self.wentry.pack(side=LEFT, fill=X, expand=1)
        self.wsend.pack(side=RIGHT)

if __name__ == '__main__':
    tk = Tk()
    tc = TelnetCommunicator(tk)
    tc.pack(fill=BOTH, expand=1)
    tk.update()
    tk.minsize(tk.winfo_width(), tk.winfo_height())
    tk.mainloop()
