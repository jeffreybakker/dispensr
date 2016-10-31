import serial
import threading
import hashlib

# Setup Variables
ARDUINO_COM = "COM3"
running = False
threads = []

# Communication Thread
class communicationThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        global running;
        # ser = serial.Serial(ARDUINO_COM, 9600)

        # Communication loop
        while running:
            # processData(ser.readline())
            continue

        # threads.remove(self)
        print("Exiting " + self.name)


# Command prompt Thread
class promptThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        global running

        # Prompt loop
        while running:
            cmd = input("> ")
            if (cmd == "exit"):
                running = False

        # threads.remove(self)
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

running = True
communication_thread = communicationThread(1, "Communication Tread")
communication_thread.start()
threads.append(communication_thread)
prompt_thread = promptThread(2, "Prompt Thread")
prompt_thread.start()
threads.append(prompt_thread)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
