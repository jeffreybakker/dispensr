import serial
import threading
import hashlib

# Setup Variables
ARDUINO_COM = "COM3"
connected = False
threads = []


# Thread
class communicationThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        ser = serial.Serial(ARDUINO_COM, 9600)

        # Communication loop
        while connected:
            processData(ser.readline())

        print("Exiting " + self.name)


# Encrypt RFID-tag
def encryptRFID(tag):
    salt = 10  # TODO: replace with database UID or something
    encrypted = hashlib.sha512(salt + tag)
    return encrypted


# Process received information
def processData(data):
    print(data)


# Main code
print("Starting Main Thread")

connected = True
comThread = communicationThread(1, "Communication thread")
comThread.start()
threads.append(comThread)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
