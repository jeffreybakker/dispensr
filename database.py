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


def setup():
    c = get_cursor()

    c.execute("CREATE TABLE Users (id INTEGER, rfid INTEGER, role VARCHAR(3), username VARCHAR(255), password VARCHAR(255))");

# CREATE TABLE Users
# (
#   	id			INTEGER(11)		PRIMARY KEY		NOT NULL,
#   	rfid		INTEGER(11)		NOT NULL 		UNIQUE,
#   	role		VARCHAR(3)		DEFAULT 'pat',
#   	username	VARCHAR			DEFAULT NULL,
#   	password	VARCHAR			DEFAULT NULL
# );
#
# CREATE TABLE Prescription
# (
#   	id			INTEGER(12)		PRIMARY KEY		NOT NULL,
#   	uid			INTEGER(11)		NOT NULL,
#   	medicine_id	INTEGER			NOT NULL,
#   	descr		TEXT,
#   	max_dose	INTEGER			NOT NULL,
#   	rec_dose	INTEGER			NOT NULL,
#   	min-time	INTEGER			NOT NULL,
#   	amount		INTEGER			NOT NULL
# );
#
# CREATE TABLE Inventory
# (
# 	id 			INTEGER			PRIMARY KEY		NOT NULL,
#   	name		VARCHAR			NOT NULL,
#   	type		VARCHAR(3)		NOT NULL,
#   	capacity	INTEGER			NOT NULL,
#   	stock		INTEGER			DEFAULT 0
# );
