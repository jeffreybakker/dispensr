import tkinter
import calendar
import time
import json
from tkinter import ttk
from tkinter.ttk import Treeview


class UIMain:
    def __init__(self, sock, function):
        root = tkinter.Tk()

        tree = Treeview(root, columns=(
        'uid', 'medicine_id', 'descr', 'max_dose', 'rec_dose', 'min_time', 'amount', 'cur_dose', 'last_time', 'doctor',
        'date', 'duration'))
        tree.heading('#0', text='id')
        tree.heading('uid', text='uid')
        tree.heading('medicine_id', text='medicine_id')
        tree.heading('descr', text='descr')
        tree.heading('max_dose', text='max_dose')
        tree.heading('rec_dose', text='rec_dose')
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
        tree.column('rec_dose', width=70)
        tree.column('min_time', width=70)
        tree.column('amount', width=70)
        tree.column('cur_dose', width=70)
        tree.column('last_time', width=70)
        tree.column('doctor', width=70)
        tree.column('date', width=70)
        tree.column('duration', width=70)

        tree.insert('', 'end', text="1", values=['3', '2', 'Tegen de hoofdpijn', '3', '5', '2', '0', '0', '0',
                                                 str(calendar.timegm(time.gmtime())), str(53135135130)])
        tree.pack()

        tosend = {}
        tosend["command"] = "getprescriptions"
        tosend["uid"] = "1"  # TODO: Hardcoded
        sock.send(json.dumps(tosend).encode())

        root.mainloop()
        function()
