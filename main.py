import threading
import hashlib
import arduino
import control
import database
import calendar
import time
from prescription import Prescription
from user import User
from preferences import Preferences
import sys

# Setup Variables
pref = Preferences()
running = False
threads = []

# Check if this is the first-run
if pref.get_preference("first_time", True):
    import sampledata

    # Set some default preferences
    pref.set_preference("first_time", False)
    pref.set_preference("database", "data/database.db")
    pref.set_preference("arduino_port", "COM3")
    pref.set_preference("notifications", False)

    # Create the database and fill it with some data
    sampledata.init()


# Communication Thread
class communicationThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global running, pref

        print("Starting " + self.name)
        database.init(pref.get_preference("database"))

        # Communication loop
        ard = arduino.Interface(b'ZxPEh7ezUDq54pRv', pref.get_preference("arduino_port"))
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
        # Fetch a user from the database with the given UID
        user = control.get_user(rfid)

        # Return a REJECT if the user was not found
        if user is None:
            print("No user found with the RFID:", rfid)
            return False

        print("User found:", user.id)

        if user.role == 'pat':
            # If the user is a patient, get all prescriptions and the inventory
            prescriptions = control.get_prescriptions(user)
            inventory = control.get_inventory()

            # Show the dispensed drugs in the terminal
            if len(prescriptions) > 0:
                print("Dispensing ", len(prescriptions), " medicine(s)")

                for pres in prescriptions:
                    for i in inventory:
                        if pres.medicine_id == i.id:
                            i.stock = i.stock - pres.amount
                            database.update_inventory(i)
                    drug = control.get_drug_by_prescription(pres)
                    print(drug.name)
                    print("\tAmount:\t" + str(pres.amount))
                    print("\tDescription:\t" + pres.descr)
                    database.commit()

            else:
                print("No prescriptions available for consumption at this moment")

        if user.role == 'ref':   # For doctor or nurse, assuming that they will only want to access the machine in order to refill it
            control.inventory_refill()
            print("Refilled the dispenser")


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
        global doctor_test
        global doctor_id
        doctor_test = False

        # Prompt loop
        while running:
            cmd = input("> ")
            if cmd == "exit":
                running = False
                database.close()
                print("Exiting now")
                sys.exit(0)

            # command for logging in with username and password if the username and password are valid
            #  doctor_test is set to true and doctor id is set to the corresponding id so the database can be edited
            if cmd == "login":
                doctors = database.get_users_by_role('doc')
                print("Please login to make changes.")
                login_username = input("Username: ")
                login_password = input("Password: ")
                for doctor in doctors:
                    if doctor.username == login_username and doctor.password == login_password:
                        doctor_id = doctor.id
                        print("Logged in as doctor id: " + str(doctor_id))
                        doctor_test = True
                if not doctor_test:
                    print("Invalid credentials!")

            # when logging out doctor test is set to false so no changes can be made
            # doctor id is set to 0 so nobody can actually see who was the last doctor to log in
            if cmd == "logout" and doctor_test:
                doctor_test = False
                print("Logged out as doctor id: " + str(doctor_id))
                doctor_id = 0

            # to update credentials you must be logged in as a doctor and you have to verify your login data again
            if cmd == "update credentials" and doctor_test:
                user = database.get_user_by_uid(doctor_id)
                print("Please verify your login.")
                login_username = input("Old username: ")
                login_password = input("Old password: ")
                if user.username == login_username and user.password == login_password:
                    new_username = input("New username = ")
                    new_password = input("New password = ")
                    user.username = new_username
                    user.password = new_password
                    database.update_user(user)
                    database.commit()
                    print("Credentials updated.")

            # to update a rfid tag you have to be logged in as a doctor and you have to input a user_id to which the new rfid will be bound
            if cmd == "update rfid" and doctor_test:
                user_id = input("User id = ")
                user = database.get_user_by_uid(user_id)
                if user is None:
                    print("No user with this id!")
                    continue

                new_rfid = input("New rfid = ")
                user.rfid = new_rfid
                database.update_user(user)
                database.commit()
                print("rfid updated.")

            # when logged in as a doctor you can get all users with their roles (but not password or rfid)
            if cmd == "get users" and doctor_test:
                users = database.get_users()
                print("id\trole")
                for user in users:
                    print(str(user.id) + "\t" + str(user.role))

            # when logged in you can get prescriptions for a single user or you can get all prescriptions
            if cmd == "get prescriptions" and doctor_test:
                choice = input("For all users y/n: ")
                prescriptions = database.get_prescriptions()
                if choice == "y":
                    print("id\tmedicine\tdescription")
                    for prescription in prescriptions:
                        print(str(prescription.id) + "\t"  + str(prescription.medicine_id) + "\t\t\t" + str(prescription.descr))
                elif choice == "n":
                    user_id = int(input("id = "))
                    print("id\tmedicine\tdescription")
                    for prescription in prescriptions:
                        if prescription.uid == user_id:
                            print(str(prescription.id) + "\t" + str(prescription.medicine_id) + "\t\t\t" + str(prescription.descr))
                else:
                    print("Invalid input!")

            # as a logged in doctor you can add prescriptions. you will be prompted for all the data
            if cmd == "add prescription" and doctor_test:
                prescriptions = database.get_prescriptions()
                prescription_list = []
                for prescription in prescriptions:
                    prescription_list.append(prescription.id)
                prescription_id = int(max(prescription_list) + 1)
                patient_id = int(input("Patient id = "))
                medicine_id = int(input("Medicine id = "))
                description = input("Description of use = ")
                max_dose = int(input("Daily max dose = "))
                min_time = int(input("Minimum time between dispenses in seconds = "))
                amount = int(input("Amount of medicine per dispense/dose = "))
                cur_dose = 0
                duration = int(input("Prescription duration in days = ")) * 86400
                date = int(calendar.timegm(time.gmtime()))

                # this part checks if the user is actually in the database else it prints "patient does not exist"
                users = database.get_users()
                patient_test = False
                for user in users:
                    if patient_id == user.id:
                        print("New prescription added with id: " + str(prescription_id))
                        database.insert_prescription(Prescription.parse_raw([prescription_id, patient_id, medicine_id, description, max_dose, min_time, amount, cur_dose, date, doctor_id, duration, date]))
                        database.commit()
                        patient_test = True
                if not patient_test:
                    print("Patient does not exist!")

            # as a logged in doctor you can remove a prescription by id
            if cmd == "remove prescription" and doctor_test:
                prescription_id = int(input("prescription id = "))
                database.remove_prescription(prescription_id)
                database.commit()
                print("Prescription removed.")

            # as a logged in doctor you can add new users. you get prompted for all data (and for username and pw if you are adding a doctor)
            if cmd == "add user" and doctor_test:
                users = database.get_users()
                user_list = []
                for user in users:
                    user_list.append(user.id)
                user_id = int(max(user_list) + 1)
                rfid = int(input("RFID = "))
                role = input("role(pat/doc/ref) = ")
                if role == 'doc':
                    new_username = input("New user username = ")
                    new_password = input("New user password = ")
                else:
                    new_username = ""
                    new_password = ""
                database.insert_user(User.parse_raw([user_id, rfid, role, new_username, new_password]))
                database.commit()
                print("New user added with id: " + str(user_id))

            # as a logged in doctor you can remove users by id
            if cmd == "remove user" and doctor_test:
                user_id = int(input("User id = "))
                database.remove_user(user_id)
                database.commit()
                print("User removed.")

            # you can always print out all existing commands
            if cmd == "help":
                commands = ["login",
                            "logout",
                            "exit",
                            "get prescriptions",
                            "add prescription",
                            "remove prescription",
                            "add user",
                            "remove user",
                            "update credentials",
                            "update rfid"]
                print("Commands:", commands)


         # threads.remove(self)
        print("Exiting " + self.name)


# Communication Thread
class TimeModel(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        # Imports
        import notification
        from concurrent.futures import thread

        # Make global variables available in local context
        global running, pref

        # Initialize everything

        database.init(pref.get_preference("database"))

        # A refill every 24 hours
        refill = 24 * 60 * 60
        sleepy_time = 5

        cur_time = int(calendar.timegm(time.gmtime()))
        last_time = cur_time - (cur_time % refill)

        # Run the code
        while running:
            # Calculate next refill
            cur_time = int(calendar.timegm(time.gmtime()))
            new = last_time + refill

            # Refill?
            if cur_time > new:
                notification.send_refill()
                control.inventory_refill()
                last_time = new
            else: # Wait till refill
                time.sleep(sleepy_time)

        database.close()


# Encrypt RFID-tag
def encryptRFID(tag):
    salt = 10  # TODO: replace with database UID or something
    encrypted = hashlib.sha512(salt + tag)


# Main code
print("Starting Main Thread")

running = True

# starting communication thread for communication with arduino
communication_thread = communicationThread(1, "Communication Thread")
communication_thread.start()
threads.append(communication_thread)

# starting TimeModel thread for notifications
time_thread = TimeModel(3, "Time Model Thread")
time_thread.start()
threads.append(time_thread)

# starting prompt thread for command prompt
prompt_thread = promptThread(2, "Prompt Thread")
prompt_thread.start()
threads.append(prompt_thread)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
