import hashlib
import socket
import sys
import json
import threading
import tkinter
from prescription import Prescription
from tkinter import messagebox
from ui_login import UILogin
from ui_loading import UILoading
from ui_main import UIMain

HOST, PORT = "127.0.0.1", 9999
running = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Encryption
def encrypt(toencr):
    salt = "duasSd9043!"  # TODO: replace with database UID or something
    return hashlib.sha512(toencr + salt)


def app_main(sock, function):
    ui_main = UIMain(sock, function)

def app_close():
    running = False
    s.shutdown(1)
    print("running = False")

# Connection thread
class connection_thread(threading.Thread):
    def __init__(self, threadID, name, sock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sock = sock

    def run(self):
        print("Starting " + self.name)
        global running

        while running:
            received = self.sock.recv(1024)
            json_data = ""

            if not received:
                print("Closing connection")
                break

            if received:
                json_data = received.decode()

            if json_data != "":
                data = json.loads(json_data)
                print(json_data)

                if data["command"] == "authlogin":
                    if data["auth"] == "True":
                        app_main(self.sock, app_close)
                    elif data["auth"] == "False":
                        #messagebox.showerror("Error", "Authentication failed")
                        print("Authentication failed")
                        running = False
                if data["command"]=="getprescriptions":
                    prescriptions = {}
                    prescriptions = Prescription.from_json_list(data["data"])


        print("Exiting " + self.name)


# Main code
try:
    s.connect((HOST, PORT))
    running = True
except socket.error as msg:
    messagebox.showerror("Error", 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

connthread = connection_thread(1, "Connection Thread", s)
connthread.start()

ui_login = UILogin(s, app_close)

connthread.join()
s.shutdown(1)
s.close()
