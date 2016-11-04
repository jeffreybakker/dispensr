# dispensr
At the moment, the *dispensr* project consists of 4 different programs:
- *arduino/RFID/*: The program that runs on the Arduino.
- *main.py*: The program that runs on a computer or server connected to the arduino
- *app/client.py*: A graphical interface for doctors or nurses (refillers)
- *app/server.py*: The backend for the graphical interface

### arduino/RFID/
This program is responsible for reading RFID-tags and communicating the data from those tags to the computer or server which runs main.py

### main.py
This program is basically the core of the system; it communicates with the arduino in order to get the RFID-tags, it manages the database and it controls how much medicine a patient may consume at a certain point in time.

### app/*
These programs, *client.py* and *server.py* are responsible for the graphical interface that a doctor or a nurse will see when he or she wants to change anything in our system. Even though there are no currently known errors in the code, this system is still not incomplete, it misses some functionality. All the functionality that it should have is already implemented in the *main.py* via the console, but that is by far not ideal. So when this project would be released to the public (or in this case hospitals and retirement homes), this system should be completely implemented so that doctors do not have to go to the computer / server the *main.py* runs on in order to change the data in our system.

## Running the code
Before running anything, *pyserial* has to be installed:
- Ubuntu `sudo pip -m install pyserial`
- Windows `pip -m install pyserial`

In the main program we have 2 scripts that can be run:
- *main.py*; the main program of this project
- *sampledata.py*; inserts some sampledata into the database for testing reasons

If you want to test the commands in the console, type `help` for a list of possible commands

**PLEASE NOTE:** *sampledata.py* should be removed from the project when releasing it to a hospital or retirement home (or any other facility that would require a drug dispenser) and any references in the code should be safely removed

Then we have the scripts in the */app/* folder, when running *client.py* and *server.py*, please make sure to start them in the following order:
1. *server.py* first, because it has to set up before the client can try to connect to it
2. *client.py* second, because when it starts, it should be able to connect to the server, when this is not the case, it will just close
