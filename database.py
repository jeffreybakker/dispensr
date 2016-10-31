import sqlite3 as sqlite

conn = None


def init(file, first_time=False):
	global conn

	if conn is not None:
		close()

	conn = sqlite.connect(file)

	if first_time:
		setup()


def close():
	global conn
	conn.commit()
	conn.close()
	conn = None


def get_cursor():
	global conn
	return conn.cursor()


def get_user_by_uid(uid):
	c = get_cursor()

	c.execute('''
        SELECT * FROM Users
        WHERE id=?
    ''', uid)


def get_user_by_rfid(rfid):
	c = get_cursor()

	c.execute('''
	        SELECT * FROM Users
	        WHERE rfid=?
	    ''', rfid)


def get_users_by_role(role):
	c = get_cursor()

	c.execute('''
            SELECT * FROM Users
            WHERE role=?
        ''', role)


def get_user_by_login(username, password):
	c = get_cursor()
	c.execute(
		'''SELECT * FROM Users WHERE username=? AND password=?''',
		username, password)


def get_users():
	c = get_cursor()
	c.execute('''SELECT * FROM Users''')


def get_prescriptions_by_uid(uid):
	c = get_cursor()

	c.execute('''
	            SELECT * FROM Prescriptions
	            WHERE uid=?
	        ''', uid)


def get_prescriptions():
	pass


def get_inventory_by_iid(iid):
	pass


def get_inventory():
	pass


def setup():
	c = get_cursor()

	c.execute('''
        DROP TABLE Inventory;
        DROP TABLE Prescription;
        DROP TABLE Users;
        
        CREATE TABLE Users
        (
            id			INTEGER(11)		PRIMARY KEY		NOT NULL,
            rfid		INTEGER(11)		NOT NULL 		UNIQUE,
            role		VARCHAR(3)		DEFAULT 'pat',
            username	VARCHAR			DEFAULT NULL,
            password	VARCHAR			DEFAULT NULL
        );
        
        CREATE TABLE Prescription
        (
            id			INTEGER(12)		PRIMARY KEY		NOT NULL,
            uid			INTEGER(11)		NOT NULL,
            medicine_id	INTEGER			NOT NULL,
            descr		TEXT,
            max_dose	INTEGER			NOT NULL,
            rec_dose	INTEGER			NOT NULL,
            min-time	INTEGER			NOT NULL,
            amount		INTEGER			NOT NULL
        );
        
        CREATE TABLE Inventory
        (
            id 			INTEGER			PRIMARY KEY		NOT NULL,
            name		VARCHAR			NOT NULL,
            type		VARCHAR(3)		NOT NULL,
            capacity	INTEGER			NOT NULL,
            stock		INTEGER			DEFAULT 0
        );''')
