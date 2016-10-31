import sqlite3 as sqlite

conn = None


def init(file):
    global conn

    if conn is not None:
        close()

    conn = sqlite.connect(file)


def close():
    global conn
    conn.commit()
    conn.close()
    conn = None


def get_cursor():
    global conn
    return conn.cursor()
