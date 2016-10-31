import sqlite3 as sqlite

class User:
    def __init__(self, id=-1, rfid=-1, role="", username="", password=""):
        self._id = id
        self._rfid = rfid
        self._role = role
        self._username = username
        self._password = password

    @staticmethod
    def parse_raw(row):
        if (row == None or len(row) != 5):
            return User()

        tempuser = User()
        tempuser.id = row[0]
        tempuser.rfid = row[1]
        tempuser.role = row[2]
        tempuser.username = row[3]
        tempuser.password = row[4]
        return tempuser

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def rfid(self):
        return self._rfid

    @rfid.setter
    def rfid(self, value):
        self._rfid = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

