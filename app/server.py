import socket
import sys
from _thread import *

HOST = '0.0.0.0'
PORT = 9999
running = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
    running = True
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(5)
print('Socket now listening')


def client_thread(conn):
    while True:
        received = conn.recv(1024)
        data = ""
        if received:
            data = received.decode()

        if data=="getdata":
            conn.send("data".encode())
        if data=="":
            print("Closing connection")
            break
        if not data:
            print("Closing connection")
            break

    conn.close()


while running:
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(client_thread, conn)

s.close()
