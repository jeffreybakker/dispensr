import socket
import sys
import json
import database
import control
from user import User
from prescription import Prescription
from inventory import Inventory
from _thread import *

HOST = '0.0.0.0'
PORT = 9999
running = False
auth = False


# Used to authenticate a user
def authenticate(username, password):
    # Make sure at least something was entered since username/password can't be empty
    if username == "" or password == "":
        return "False"

    database.init("../data/database.db")

    print(username + "," + password)
    # Get a user object belonging to the entered credentials
    user = database.get_user_by_login(username, password)

    # If the user object is not null, the credentials are valid
    if not user:
        return "False"
    else:
        return "True"

    database.close()


# Each client gets assigned a new thread that listens to it
def client_thread(conn):
    # Loop indefinitively
    while True:
        # This blocks the loop untill something is received
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
            # The messages use the JSON format
            data = json.loads(json_data)

            # The command is 'login', authenticate the credentials and send back the result
            if data["command"] == "login":
                tosend = {}
                tosend["command"] = "authlogin"
                tosend["auth"] = authenticate(data["username"], data["password"])
                if (tosend["auth"] == "True"):
                    auth = True
                print("Sending: " + json.dumps(tosend))
                conn.send(json.dumps(tosend).encode())

            # The command is 'getprescriptions', get the prescriptions of the user and compress them to a string
            # in JSON format
            if data["command"] == "getprescriptions" and auth:
                user = database.get_user_by_uid(data["uid"])
                print("Info: " + str(user.id) + ", " + str(user.username) + ", " + str(user.rfid))
                prescriptions = user.get_prescriptions()
                tosend = {}
                tosend["command"] = "getprescriptions"
                tosend["data"] = Prescription.to_json_list(prescriptions)
                print("Sending: " + str(tosend))
                conn.send(json.dumps(tosend).encode())

    # Properly close the connection, shutdown notifies the client that is should stop listening
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

# Listen to incomming connections, the server supports up to five connections simultaniously
s.listen(5)
print('Socket now listening')

# Loop
while running:
    # Blocks thread untill client connects
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    # Creates thread for that client
    start_new_thread(client_thread, (conn,))

# End
s.shutdown(1)
s.close()
