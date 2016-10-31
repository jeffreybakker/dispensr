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

    conn = sqlite.connect(file)

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
        '''INSERT INTO User (id, rfid, role, username, password) VALUES (id = ?, rfid = ?, role = ?, username = ?, password = ?)''',
        (user.id, user.rfid, user.role, user.username, user.password))


def get_user_by_uid(uid):
    """\
    Returns an <User> object for the user with the given uid

    :param uid: An unique integer that represents the userID
    :return: An <User> object for the given uid, None if the user was not found
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users WHERE id=?''', uid)

    if cursor.rowCount == 0:
        return None

    return User.parse_raw(cursor.fetchone())


def get_user_by_rfid(rfid):
    """
    Returns an <User> object for the user with the given rfid

    :param rfid: The ID of the RFID tag of the user
    :return: An <User> object for the given rfid, None if no user was found
    """
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users WHERE rfid=?''', rfid)

    if cursor.rowCount == 0:
        return None

    return User.parse_raw(cursor.fetchone())


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
    c = get_cursor()
    cursor = c.execute(
        '''SELECT * FROM Users WHERE username=? AND password=?''',
        (username, password))

    if cursor.rowCount == 0:
        return None

    return User.parse_raw(cursor.fetchone())


def get_users():
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Users''')

    res = []

    for row in cursor:
        res.append(User.parse_raw(row))

    return res


def insert_prescription(prescription):
    """
    Inserts an <Prescription> object into the database

    :param prescription: An object of the <Prescription> type
    """
    c = get_cursor()
    c.execute(
        '''INSERT INTO Prescription (id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount) VALUES (id = ?, uid = ?, medicine_id = ?, descr = ?, max_dose = ?, rec_dose = ?, min_time = ?, amount = ?)''',
        (prescription.id, prescription.uid, prescription.medicine_id, prescription.descr, prescription.max_dose, prescription.rec_dose, prescription.min_time, prescription.amount))


def get_prescriptions_by_uid(uid):
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Prescriptions WHERE uid=?''', uid)

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def get_prescriptions():
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Prescriptions''')

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def insert_inventory(drug):
    """
    Inserts an <Inventory> object into the database

    :param drug: An object of the <Inventory> type
    """
    c = get_cursor()
    c.execute(
        '''INSERT INTO Inventory (id, name, type, capacity, stock) VALUES (id = ?, name = ?, type = ?, capacity = ?, stock = ?)''',
        (drug.id, drug.name, drug.type, drug.capacity, drug.stock))


def get_inventory_by_iid(iid):
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Inventory WHERE id=?''', iid)

    if cursor.rowCount == 0:
        return None

    return Inventory.parse_raw(cursor.fetchone())


def get_inventory():
    c = get_cursor()
    cursor = c.execute('''SELECT * FROM Inventory''')

    res = []

    for row in cursor:
        res.append(Prescription.parse_raw(row))

    return res


def _setup():
    c = get_cursor()
    c.execute("DROP TABLE IF EXISTS Inventory")
    c.execute("DROP TABLE IF EXISTS Prescription")
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
        CREATE TABLE Prescription
        (
            id			INTEGER(12)		PRIMARY KEY		NOT NULL,
            uid			INTEGER(11)		NOT NULL,
            medicine_id	INTEGER			NOT NULL,
            descr		TEXT,
            max_dose	INTEGER			NOT NULL,
            rec_dose	INTEGER			NOT NULL,
            min_time	INTEGER			NOT NULL,
            amount		INTEGER			NOT NULL
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
