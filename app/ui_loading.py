import tkinter
from tkinter import ttk

class UILoading:
    def __init__(self, root):
        ft = ttk.Frame()
        ft.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
        pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
        pb_hD.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
        pb_hD.start(50)
        root.mainloop()

if __name__ == "__main__":
    UILoading(tkinter.Tk())