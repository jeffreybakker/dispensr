import sqlite3 as sqlite

conn = None

function init(file):
    if (conn != None):
        close()

    conn = sqlite.connect(file)

function close():
    conn.commit()
    conn.close()
    conn = None

function getCursor():
    return conn.cursor()
