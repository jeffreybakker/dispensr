import hashlib
import socket
import sys
import json
import threading
import tkinter
import queue
import time
from prescription import Prescription
from tkinter import messagebox
from ui_login import UILogin
from ui_loading import UILoading
from ui_main import UIMain

HOST, PORT = "127.0.0.1", 9999
running = False
blocking = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
prescriptions = None
uid = -1

def app_set_uid(value):
    global uid
    uid = value
    print('uid set')

def app_close():
    running = False
    s.shutdown(1)
    print("running = False")


def app_main(sock, func_close, func_queue):
    print("executing app_main")
    ui_main = UIMain(sock, func_close, func_queue)


def unblock_main():
    global blocking
    blocking = False
    print("Unblocking Main Thread")


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
                print("Received: " + str(json_data))

                if data["command"] == "authlogin":
                    if data["auth"] == "True":
                        tosend = {}
                        tosend["command"] = "getprescriptions"
                        tosend["uid"] = uid  # TODO: Hardcoded
                        print("Sending: " + str(json.dumps(tosend)))
                        self.sock.send(json.dumps(tosend).encode())
                    elif data["auth"] == "False":
                        # messagebox.showerror("Error", "Authentication failed")
                        print("Authentication failed")
                        running = False
                if data["command"] == "getprescriptions":
                    global prescriptions
                    prescriptions = {}
                    prescriptions = Prescription.from_json_list(data["data"])
                    from_dummy_thread(lambda : {unblock_main()})



        print("Exiting " + self.name)
        from_dummy_thread(lambda: unblock_main())


# Queue Code
callback_queue = queue.Queue()


def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)


def from_main_thread_blocking():
    callback = callback_queue.get()  # blocks until an item is available
    callback()


def from_main_thread_nonblocking():
    print("nonblocking")
    while True:
        try:
            callback = callback_queue.get(False)  # doesn't block
        except queue.Empty:  # raised when queue is empty
            break
        callback()


def update_queue():
    from_main_thread_blocking()


# Main Code
try:
    s.connect((HOST, PORT))
    running = True
except socket.error as msg:
    messagebox.showerror("Error", 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

connthread = connection_thread(1, "Connection Thread", s)
connthread.start()
ui_login = UILogin(s, app_close, app_set_uid)

blocking = True
print("Blocking Main Thread")
while blocking:
    from_main_thread_blocking()
print("Stopped blocking Main Thread")

UIMain(s, app_close, prescriptions)


connthread.join()
s.shutdown(1)
s.close()

