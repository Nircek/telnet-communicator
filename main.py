#!/usr/bin/env python3
from tkinter import Tk, Frame, Text, Entry, Button, TOP, LEFT, RIGHT, BOTH, X, END
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class TelnetClient:
    TYPE_ADDRESS = b'Please type the address of the server.\n'
    TYPE_PORT = b'Please type the port number.\n'
    PORT_IS_INT = b'The port number should be an integer value.\n'
    DISCONNECTED = b'You are disconnected.\n'
    RECONNECT = b'Reconnect? [y/n]\n'
    def __init__(self, callback, host=None, port=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.connected = False
    def handleMsg(self):
        while True:
            s = self.socket.recv(2**10)
            if s:
                self.callback(s)
            else:
                self.connected = False
                self.callback(self.DISCONNECTED+self.RECONNECT)
                break
    def handle(self):
        if self.host is None:
            self.callback(self.TYPE_ADDRESS)
        elif self.port is None:
            self.callback(self.TYPE_PORT)
        else:
            try:
                self.socket.connect((self.host, self.port))
                self.connected = True
                self.thread = Thread(target=self.handleMsg, daemon=True)
                self.thread.start()
            except ConnectionRefusedError:
                self.callback(self.DISCONNECTED+self.RECONNECT)
    def send(self, msg):
        if self.host is None:
            self.host = msg
            self.handle()
        elif self.port is None:
            try:
                self.port = int(msg)
            except ValueError:
                self.callback(self.PORT_IS_INT)
            self.handle()
        elif not self.connected:
            if msg == b'y':
                self.handle()
            elif msg == b'n':
                self.host, self.port = None, None
                self.handle()
            else:
                self.callback(self.RECONNECT)
        else:
            self.socket.sendall(msg+b'\n')

class TelnetCommunicator(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.wtext = Text(self, width=40, height=10)
        self.wentry = Entry(self)
        self.wentry.bind('<Return>', lambda x: self.csend())
        self.wsend = Button(self, text='SEND', command=self.csend)
        self.wtext.pack(side=TOP, fill=BOTH, expand=1)
        self.wentry.pack(side=LEFT, fill=X, expand=1)
        self.wsend.pack(side=RIGHT)
        self.tc = TelnetClient(self.crecv)
        self.tc.handle()

    def csend(self):
        s = self.wentry.get()
        self.tc.send(s.encode())
        self.wentry.delete(0, END)

    def crecv(self, msg):
        self.wtext.insert(END, msg.decode())

if __name__ == '__main__':
    tk = Tk()
    tc = TelnetCommunicator(tk)
    tc.pack(fill=BOTH, expand=1)
    tk.update()
    tk.minsize(tk.winfo_width(), tk.winfo_height())
    tk.mainloop()
