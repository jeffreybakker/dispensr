import socket
import sys
import json
import database
from user import User
from prescription import Prescription
from inventory import Inventory
from _thread import *

HOST = '0.0.0.0'
PORT = 9999
running = False
auth = False


def authenticate(username, password):
    database.init("../data/database.db")

    print(username + "," + password)
    user = database.get_user_by_login(username, password)

    if user.id == -1:
        return "False"
    else:
        return "True"

    database.close()


def client_thread(conn):
    while True:
        received = conn.recv(1024)
        json_data = ""

        # Received == None
        if not received:
            print("Closing connection")
            break

        # Something was received, decode it
        if received:
            json_data = received.decode()

        # The decoded message is not empty, analyse it
        if json_data != "":
            data = json.loads(json_data)

            if data["command"] == "login":
                tosend = {}
                tosend["command"] = "authlogin"
                tosend["auth"] = authenticate(data["username"], data["password"])
                if (tosend["auth"] == "True"):
                    auth = True
                s.send(json.dumps(tosend).encode())

    # Properly close the connection
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
