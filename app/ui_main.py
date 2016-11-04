import tkinter
import calendar
import time
import json
from tkinter import ttk
from tkinter.ttk import Treeview


class UIMain:
    def __init__(self, sock, prescriptions):
        # Create the window
        root = tkinter.Tk()

        # Create the table
        tree = Treeview(root, columns=(
            'uid', 'medicine_id', 'descr', 'max_dose', 'min_time', 'amount', 'cur_dose', 'last_time',
            'doctor',
            'date', 'duration'))
        tree.heading('#0', text='id')
        tree.heading('uid', text='uid')
        tree.heading('medicine_id', text='medicine_id')
        tree.heading('descr', text='descr')
        tree.heading('max_dose', text='max_dose')
        tree.heading('min_time', text='min_time')
        tree.heading('amount', text='amount')
        tree.heading('cur_dose', text='cur_dose')
        tree.heading('last_time', text='last_time')
        tree.heading('doctor', text='doctor')
        tree.heading('date', text='date')
        tree.heading('duration', text='duration')

        tree.column('#0', width=40)
        tree.column('uid', width=40)
        tree.column('medicine_id', width=70)
        tree.column('descr', width=70)
        tree.column('max_dose', width=70)
        tree.column('min_time', width=70)
        tree.column('amount', width=70)
        tree.column('cur_dose', width=70)
        tree.column('last_time', width=70)
        tree.column('doctor', width=70)
        tree.column('date', width=70)
        tree.column('duration', width=70)

        # Insert the data
        for i in range(0, len(prescriptions)):
            tree.insert('', 'end', text=prescriptions[i].id,
                        values=[prescriptions[i].uid, prescriptions[i].medicine_id, prescriptions[i].descr,
                                prescriptions[i].max_dose, prescriptions[i].min_time, prescriptions[i].amount,
                                prescriptions[i].cur_dose, prescriptions[i].last_time, prescriptions[i].doctor,
                                prescriptions[i].date, prescriptions[i].duration])

        tree.pack()

        # Run the mainloop
        root.mainloop()

        # ^^ Here i ran in to a problem since this means the 'main thread' (as in client.py) can't notify this class
        # of certain events because this ui technically runs on the main thread.
        # Therefore, in order to add functionality such as changing prescriptions, which would need to combine
        # this thread for receiving the ui events, the connection thread for handling the responses from the server
        # and the main thread for communication between the two threads, is not possible in this version of the code
        # Unfortunately there was not enough time to finish this UI
        # (also running this class on a seperate thread severely increases the difficulty of letting all
        # threads communicate with each other without



