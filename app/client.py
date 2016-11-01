import socket
import tkinter

HOST, PORT = "127.0.0.1", 9999
running = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def button_callback():
    print("button clicked")
    sock.send("getdata".encode())

try:
    sock.connect((HOST, PORT))
    sock.send("getdata".encode())
    print(sock.recv(1024))
    running = True

    #top = tkinter.Tk()
    #button = tkinter.Button(top, text="getdata", command=button_callback)
    #button.pack()
    #top.mainloop()

    #received = sock.recv(1024)
finally:
    sock.close()