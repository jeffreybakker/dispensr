import sqlite3 as sqlite

conn = None


def init(file, first_time=False):
    global conn

    if conn is not None:
        close()

    conn = sqlite.connect(file)

    if first_time:
        _setup()
        conn.commit()


def close():
    global conn
    conn.commit()
    conn.close()
    conn = None


def get_cursor():
    global conn
    return conn.cursor()


def insert_user(id, rfid, role, username, password):
    c = get_cursor()
    c.execute(
        '''INSERT INTO User (id, rfid, role, username, password) VALUES (id = ?, rfid = ?, role = ?, username = ?, password = ?)''',
        id, rfid, role, username, password)


def get_user_by_uid(uid):
    c = get_cursor()
    c.execute('''SELECT * FROM Users WHERE id=?''', uid)


def get_user_by_rfid(rfid):
    c = get_cursor()
    c.execute('''SELECT * FROM Users WHERE rfid=?''', rfid)


def get_users_by_role(role):
    c = get_cursor()
    c.execute('''SELECT * FROM Users WHERE role=?''', role)


def get_user_by_login(username, password):
    c = get_cursor()
    c.execute(
        '''SELECT * FROM Users WHERE username=? AND password=?''',
        username, password)


def get_users():
    c = get_cursor()
    c.execute('''SELECT * FROM Users''')


def insert_prescription(id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount):
	c = get_cursor()

	c.execute('''INSERT INTO Prescriptions (id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount) VALUES (id = ?, uid = ?, medicine_id = ?, descr = ?, max_dose = ?, rec_dose = ?, min_time = ?, amount = ?)''',
			  id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount)


def get_prescriptions_by_uid(uid):
    c = get_cursor()
    c.execute('''SELECT * FROM Prescriptions WHERE uid=?''', uid)


def get_prescriptions():
    c = get_cursor()
    c.execute('''SELECT * FROM Prescriptions''')


def get_inventory_by_iid(iid):
    c = get_cursor()
    c.execute('''SELECT * FROM Inventory WHERE id=?''', iid)


def get_inventory():
    c = get_cursor()
    c.execute('''SELECT * FROM Inventory''')


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
