import tkinter
import json
from tkinter import *


class UILogin:

    # Login button callback
    def button_login_callback(self):
        data = {}
        data['command'] = 'login'
        data['username'] = self.entry_user.get()
        data['password'] = self.entry_password.get()
        print(json.dumps(data))
        self.socket.send(json.dumps(data).encode())
        self.keepAlive = True
        self.close()

    def __init__(self, socket, function):
        self.socket = socket
        self.keepAlive = False

        # Root of window
        self.root = tkinter.Tk()
        frame_login = Frame(self.root)
        frame_login.pack(side=TOP)
        frame_button = Frame(self.root)
        frame_button.pack(side=BOTTOM)

        # Login Frames
        frame_label = Frame(frame_login)
        frame_label.pack(side=LEFT)
        frame_entry = Frame(frame_login)
        frame_entry.pack(side=RIGHT)

        # Login fields and entries
        label_user = Label(frame_label, text="Username", width=16)
        label_user.pack()
        label_password = Label(frame_label, text="Password", width=16)
        label_password.pack()
        self.entry_user = Entry(frame_entry)
        self.entry_user.pack()
        self.entry_password = Entry(frame_entry)
        self.entry_password.pack()

        # Login Button
        labelframe_buttonspacer = LabelFrame(frame_button, height=16)
        labelframe_buttonspacer.pack()
        button_login = Button(frame_button, text="Login", width=7, command=self.button_login_callback)
        button_login.pack()

        self.root.mainloop()
        if not self.keepAlive:
            function()

    def close(self):
        self.root.destroy()


if __name__ == "__main__":
    ui = UILogin(None)
