import tkinter
import calendar
import time
import json
from tkinter import ttk
from tkinter.ttk import Treeview


class UIMain:
    def __init__(self, sock, func_close, prescriptions):
        root = tkinter.Tk()

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

        for i in range(0, len(prescriptions)):
            tree.insert('', 'end', text=prescriptions[i].id,
                        values=[prescriptions[i].uid, prescriptions[i].medicine_id, prescriptions[i].descr,
                                prescriptions[i].max_dose, prescriptions[i].min_time, prescriptions[i].amount,
                                prescriptions[i].cur_dose, prescriptions[i].last_time, prescriptions[i].doctor,
                                prescriptions[i].date, prescriptions[i].duration])

        tree.pack()

        root.mainloop()
        func_close()

    def update_tree(self, prescriptions):
        print("im update tree")
        pass
