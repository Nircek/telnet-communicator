#!/usr/bin/env python3
from tkinter import Tk, Frame, Button

class TelnetCommunicator(Frame):
    def __init__(self, master):
        super().__init__(master)

if __name__ == '__main__':
    tk = Tk()
    tc = TelnetCommunicator(tk)
    tc.pack()
    tk.mainloop()
