import threading
import hashlib
import arduino
import control
import database

# Setup Variables
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
        global running
        database.init("data/database.db")

        # Communication loop
        ard = arduino.Interface(b'ZxPEh7ezUDq54pRv', 'COM3')
        while running:
            if self._scanned_card(ard.read_rfid()):
                ard.send_accept()
            else:
                ard.send_reject()

        # threads.remove(self)
        print("Exiting " + self.name)
        database.close()

    @staticmethod
    def _scanned_card(rfid):
        user = control.get_user(rfid)

        if user is None:
            print("No user found with the RFID:", rfid)
            return False

        if user.role == 'pat':
            prescriptions = control.get_prescriptions(user)

            if len(prescriptions) > 0:
                print("Dispensing", len(prescriptions), "medicines")

                for pres in prescriptions:
                    drug = control.get_drug_by_prescripiton(pres)
                    print(drug.name)
                    print("\tAmount:\t" + pres.amount)
                    print("\tDescription:\t" + pres.descr)

            else:
                print("No prescriptions available for consumption at this moment")

        else:   # For doctor or nurse, assuming that they will only want to access the machine in order to refill it
            control.inventory_refill()

        return True


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
            if cmd == "exit":
                running = False

        # threads.remove(self)
        print("Exiting " + self.name)


# Encrypt RFID-tag
def encryptRFID(tag):
    salt = 10  # TODO: replace with database UID or something
    encrypted = hashlib.sha512(salt + tag)


# Main code
print("Starting Main Thread")

running = True
communication_thread = communicationThread(1, "Communication Thread")
communication_thread.start()
threads.append(communication_thread)
prompt_thread = promptThread(2, "Prompt Thread")
prompt_thread.start()
threads.append(prompt_thread)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
