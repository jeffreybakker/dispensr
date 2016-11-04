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
from ui_main import UIMain

HOST, PORT = "127.0.0.1", 9999
running = False
blocking = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
prescriptions = None
uid = -1


# This function is used so that the UILogin can pass the UID to the main thread
def app_set_uid(value):
    global uid
    uid = value
    print('uid set')


# Set running to False so that the loops of all threads stop
# Send the shutdown signal so that socket.recv stops blocking the threads (otherwise they wont exit)
def app_close():
    running = False
    s.shutdown(1)
    print("running = False")


# Stop the Queue from blocking the main thread (see bottom for further explanation)
def unblock_main():
    global blocking
    blocking = False
    print("Unblocking Main Thread")


# Thread used to continuously receive data
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
                # Messages are send in JSON format
                data = json.loads(json_data)
                print("Received: " + str(json_data))

                if data["command"] == "authlogin":
                    if data["auth"] == "True":
                        # When the server accepts the login request, send a new request to the server in order to retrieve the prescriptions of the patient
                        tosend = {}
                        tosend["command"] = "getprescriptions"
                        print("uid: " + str(uid))
                        tosend["uid"] = uid
                        print("Sending: " + str(json.dumps(tosend)))
                        self.sock.send(json.dumps(tosend).encode())
                    elif data["auth"] == "False":
                        # The authentication failed (because of wrong credentials), exit the program
                        # messagebox.showerror("Error", "Authentication failed")
                        print("Authentication failed")
                        running = False
                        s.shutdown(1)
                if data["command"] == "getprescriptions":
                    # The request to retrieve the prescriptions has been answered, convert them to prescription objects and notify the main thread
                    global prescriptions
                    prescriptions = {}
                    prescriptions = Prescription.from_json_list(data["data"])
                    from_dummy_thread(lambda: {unblock_main()})

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


# Main Code
try:
    s.connect((HOST, PORT))
    running = True
except socket.error as msg:
    messagebox.showerror("Error", 'Connection failed.')
    sys.exit()

# Start the thread that listens to the socket
connthread = connection_thread(1, "Connection Thread", s)
connthread.start()
# Start the login ui to get the credentials of the user, this will then send the authentication request and close itself so that the main thread can continue
# So important to note is that the UILogin runs on the main thread, which means that the code beneath it is only ran
# once the UILogin is closed (by entering the credentials and pressing login, or pressing the x button)
# Note: app_close is passed on so that UILogin can set running to false in order to prevent the program from continuing
# Note app_set_uid is passed on so that UILogin can pass on the uid of which the prescriptions have to be read
UILogin(s, app_close, app_set_uid)

blocking = True
print("Blocking Main Thread")
while blocking:
    # This will stop the main thread from going past this while loop.
    # from_main_thread_blocking will keep checking the Queue
    # once the connection thread receives an answer to the authentication request, it will add the unblock_main() method
    # to the Queue, which will set blocking to false and stop from_main_thread_blocking() from blocking the main thread
    from_main_thread_blocking()
print("Stopped blocking Main Thread")

# If no exit signal has been given yet, e.g. if the wrong credentials were entered, continue the program by opening
# the main ui
# Note: prescriptions is passed on so that the Main UI has data to display
if running:
    UIMain(s, prescriptions)
    app_close()

# Wait for the thread to close
# Note: if the connection thread is not properly notified that the program want to exit, e.g. no shutdown signal is given,
# it will prevent the program from exiting
connthread.join()
# just to be sure
s.shutdown(1)
# close the socket
s.close()
