# dispensr
At the moment, our project consists of 4 different programs which can run simultaniousely, namely:
- The main script (main.py), this script is responsible for communicating with the arduino and outputting to the console when a patient has scanned his or her card
- The program on the arduino (arduino/RFID/), this is the program that runs on the arduino; it reads the UIDs from the rfid-tags and sends encrypted data to the main program and then outputs to the LEDs depending on what resultcode was received from the main program
- Interface server (app/server.py) which handles the communication between an interface (for doctors or nurses) and the database
- Interface client (app/client.py) which displays information from the database to the user and sends user-actions to the server for processing. Some of these actions are: Logging in, viewing / editing the prescriptions per patient, adding or removing patients or editing any user data (for as far as the user's permissions allow it)

PLEASE NOTE: Before running any of these programs, the sampledata must be loaded into the database by running sampledata.py

NOTE 2: If you want to run the client, please make sure you have the server running on the background first.

# Current functionality
At this moment in time, the function of some of the programs are somewhat limited, for example, the main program does output everything according to the requirements, but it still outputs some debugging messages. Also the server and client applications aren't completed yet.
