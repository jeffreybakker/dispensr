import sqlite3 as sqlite

from inventory import Inventory
from prescription import Prescription
from user import User

conn = None


def init(file, first_time=False):
    """\
    init(file_name[, first_time])

    Opens the database file for reading and writing.
    If first_time is set to True it will also run setup the database
    for use
    """
    global conn

    if conn is not None:
        close()

    conn = sqlite.connect(file, check_same_thread=False)

    if first_time:
        _setup()
        conn.commit()


def close():
    """\
    Commits all data changes and closes the database
    """
    global conn
    commit()
    conn.close()
    conn = None


def get_cursor():
    """\
    Gets the cursor for the current database-connection

    :return: Returns the cursor for the current database-connection
    """
    global conn
    return conn.cursor()


def commit():
    """
    Commits all database changes made since the last commit
    """
    global conn
    conn.commit()


def insert_user(user):
    """\
    Inserts an <User> object into the database

    :param user: An object of the <User> type
    """
    c = get_cursor()
    c.execute(
        '''INSERT INTO Users (id, rfid, role, username, password) VALUES (?, ?, ?, ?, ?)''',
        (user.id, user.rfid, user.role, user.username, user.password))


def update_user(user):
    """\
    Updates the user entry in the database

    :param user: The <User> object that has to be updated in the database
    """
    c = get_cursor()
    c.execute(
        '''UPDATE Users SET rfid=?, role='?', username='?', password='?' WHERE id=?''',
        (user.rfid, user.role, user.username, user.password))


def uid_available(uid):
    """\
    Checks if a given UID is possible for usage

    :param uid: An integer representing the UID to be checked
    :return: A boolean indicating whether the UID is available or not
    """
    c = get_cursor()
    cursor = c.execute('''SELECT id FROM Users WHERE id=?''', uid)

    if cursor.fetchone is None:
        return False

    return True


def get_user_by_uid(uid):
    """\
    Returns an <User> object for the user with the given uid

    :param uid: An unique integer that represents the userID
    :return: An <User> object for the given uid, None if the user was not found
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users WHERE id=?''', uid)

    row = cursor.fetchone()

    if row is None:
        return None

    return User.parse_raw(row)


def get_user_by_rfid(rfid):
    """
    Returns an <User> object for the user with the given RFID

    :param rfid: The ID of the RFID tag of the user
    :return: An <User> object for the given rfid, none if no user was found
    """
    c = get_cursor()
    cursor = c.execute(
        '''SELECT * FROM Users WHERE rfid=?;''',
        (rfid,))

    row = cursor.fetchone()

    if row is None:
        return None

    return User.parse_raw(row)


def get_users_by_role(role):
    """
    Returns a list of all users with a certain role

    :param role: A String of either 'pat', 'doc' or 'ref'
    :return:
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users WHERE role=?''', role)

    res = []

    for row in cursor:
        res.append(User.parse_raw(row))

    return res


def get_user_by_login(username, password):
    """\
    Returns the user with the given credentials

    :param username: The username of the requested user
    :param password: The (encrypted / hashed) password of the requested user
    :return: The requested user, or None if the credentials are incorrect
    """
    c = get_cursor()
    cursor = c.execute(
        '''SELECT * FROM Users WHERE username=? AND password=?''',
        (username, password))

    row = cursor.fetchone()

    if row is None:
        return None

    return User.parse_raw(row)


def get_users():
    """\
    Returns all the users

    :return: A list of <User> objects
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users''')

    res = []

    for row in cursor:
        res.append(User.parse_raw(row))

    return res


def first_available_pid():
    """\
    Returns the first available pid for the database

    :return: An integer for the first not-taken PID
    """
    c = get_cursor()
    cursor = c.execute('''SELECT id FROM Prescriptions ORDER BY id DESC LIMIT 1''')

    row = cursor.fetchone()

    if row is None:
        return 0

    return row[0] + 1


def insert_prescription(prescription):
    """\
    Inserts an <Prescription> object into the database

    :param prescription: An object of the <Prescription> type
    """
    c = get_cursor()
    c.execute(
        '''INSERT INTO Prescriptions (id, uid, medicine_id, descr, max_dose, min_time, amount, cur_dose, last_time, doctor, date, duration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (prescription.id, prescription.uid, prescription.medicine_id, prescription.descr, prescription.max_dose, prescription.min_time, prescription.amount, prescription.cur_dose, prescription.last_time, prescription.doctor, prescription.date, prescription.duration))


def update_prescription(prescription):
    c = get_cursor()
    c.execute(
        '''UPDATE Prescriptions SET medicine_id=?, descr=?, max_dose=?, min_time=?, amount=?, cur_dose=?, last_time=?, doctor=?, date=?, duration=? WHERE id=?''',
        (prescription.medicine_id, prescription.descr, prescription.max_dose, prescription.min_time, prescription.amount, prescription.cur_dose, prescription.last_time, prescription.doctor, prescription.date, prescription.duration, prescription.id))


def get_prescriptions_by_uid(uid):
    """\
    Returns a list of prescriptions for a certain patient

    :param uid: The userID of the patient
    :return: A list of <Prescription> objects for the given uid
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Prescriptions WHERE uid=?''', (uid,))

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def get_prescriptions():
    """\
    Returns a list of all the prescriptions known in the database

    :return: A list of <Prescription> objects
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Prescriptions''')

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def insert_inventory(drug):
    """\
    Inserts an <Inventory> object into the database

    :param drug: An object of the <Inventory> type
    """
    c = get_cursor()
    c.execute(
        '''INSERT INTO Inventory (id, name, type, capacity, stock) VALUES (?, ?, ?, ?, ?)''',
        (drug.id, drug.name, drug.type, drug.capacity, drug.stock))


def update_inventory(drug):
    c = get_cursor()
    c.execute(
        '''UPDATE Inventory SET name='?', type='?', capacity=?, stock=? WHERE id=?''',
        (drug.name, drug,type, drug.capacity, drug.stock, drug.id))


def first_available_iid():
    """\
    Returns the first available iid for the database

    :return: An integer for the first not-taken IID
    """
    c = get_cursor()
    cursor = c.execute('''SELECT id FROM Inventory ORDER BY id DESC LIMIT 1''')

    row = cursor.fetchone()

    if row is None:
        return 0

    return row[0] + 1


def get_inventory_by_iid(iid):
    """\
    Returns the <Inventory> object for the given drug ID

    :param iid: The drug ID
    :return: An <Inventory> object for the given drug ID
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Inventory WHERE id=?''', (iid,))

    row = cursor.fetchone()

    if row is None:
        return None

    return Inventory.parse_raw(row)


def get_inventory():
    """\
    Returns a list of all <Inventory> objects in the database

    :return: A list of <Inventory> objects
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Inventory''')

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def _setup():
    """\
    Sets up the database for use
    """
    c = get_cursor()
    c.execute("DROP TABLE IF EXISTS Inventory")
    c.execute("DROP TABLE IF EXISTS Prescriptions")
    c.execute("DROP TABLE IF EXISTS Users")

    c.execute("""\
        CREATE TABLE Users
        (
            id			INTEGER(11)		PRIMARY KEY		NOT NULL,
            rfid		INTEGER(11)		NOT NULL 		UNIQUE,
            role		VARCHAR(3)		DEFAULT 'pat',
            username	VARCHAR			DEFAULT NULL,
            password	VARCHAR			DEFAULT NULL
        )""")

    c.execute("""\
        CREATE TABLE Prescriptions
        (
            id			INTEGER(12)		PRIMARY KEY		NOT NULL,
            uid			INTEGER(11)		NOT NULL,
            medicine_id	INTEGER			NOT NULL,
            descr		TEXT,
            max_dose	INTEGER	        DEFAULT -1,
            min_time	INTEGER			NOT NULL,
            amount		INTEGER			NOT NULL,
            cur_dose    INTEGER         NOT NULL,
            last_time   INTEGER(32)     NOT NULL,
            doctor      INTEGER         NOT NULL,
            date        INTEGER(32)     NOT NULL,
            duration    INTEGER(32)     DEFAULT 3153600000
        )""")

    c.execute("""\
        CREATE TABLE Inventory
        (
            id 			INTEGER			PRIMARY KEY		NOT NULL,
            name		VARCHAR			NOT NULL,
            type		VARCHAR(3)		NOT NULL,
            capacity	INTEGER			NOT NULL,
            stock		INTEGER			DEFAULT 0
        )""")
