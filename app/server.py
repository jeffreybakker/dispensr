import socket
import sys
import json
import database
from _thread import *

HOST = '0.0.0.0'
PORT = 9999
running = False

def authenticate(username, password):
    database.init("database.db", True)
    user = database.get_user_by_login(username, password)

    if user:
        return "True"
    else:
        return "False"

def client_thread(conn):
    while True:
        received = conn.recv(1024)
        json_data = ""

        if not received:
            print("Closing connection")
            break

        if received:
            json_data = received.decode()

        if json_data != "":
            data = json.loads(json_data)

            if data["command"] == "login":
                tosend = {}
                tosend["command"] = "authlogin"
                tosend["auth"] = authenticate(data["username"], data["password"])

    conn.shutdown(1)
    conn.close()

# Main code
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
    running = True
except socket.error as msg:
    print("Bind failed")
    sys.exit()

print('Socket bind complete')

s.listen(5)
print('Socket now listening')

# Loop
while running:
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(client_thread, (conn,))

# End
s.shutdown(1)
s.close()
