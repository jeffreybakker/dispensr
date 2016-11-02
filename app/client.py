import socket
import sys
import tkinter
from _thread import *

HOST, PORT = "127.0.0.1", 9999
running = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Button callback
def button_callback():
    print("button clicked")
    s.send("getdata".encode())


# Connection thread
def connection_thread(sock):
    while running:
        print(sock.recv(1024))
    sock.close()


# Main code
try:
    s.connect((HOST, PORT))
    running = True
    start_new_thread(connection_thread, (s,))
except socket.error as msg:
    print('Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

top = tkinter.Tk()
button = tkinter.Button(top, text="getdata", command=button_callback)
button.pack()
top.mainloop()

# received = sock.recv(1024)
