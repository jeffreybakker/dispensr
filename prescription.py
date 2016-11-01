class Prescription:
    def __init__(self, id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount, cur_dose, last_time):
        self._id = id
        self._uid = uid
        self._medicine_id = medicine_id
        self._descr = descr
        self._max_dose = max_dose
        self._rec_dose = rec_dose
        self._min_time = min_time
        self._amount = amount
        self._cur_dose = cur_dose
        self._last_time = last_time

    @staticmethod
    def parse_raw(row):
        if row is None or len(row) != 8:
            return Prescription()

        tempprescription = Prescription()
        tempprescription.id = row[0]
        tempprescription.uid = row[1]
        tempprescription.medicine_id = row[2]
        tempprescription.descr = row[3]
        tempprescription.max_dose = row[4]
        tempprescription.rec_dose = row[5]
        tempprescription.min_time = row[6]
        tempprescription.amount = row[7]
        tempprescription.cur_dose = row[8]
        tempprescription.last_time = row[9]
        return tempprescription

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def medicine_id(self):
        return self._medicine_id

    @medicine_id.setter
    def medicine_id(self, value):
        self._medicine_id = value

    @property
    def descr(self):
        return self._descr

    @descr.setter
    def descr(self, value):
        self._descr = value

    @property
    def max_dose(self):
        return self._max_dose

    @max_dose.setter
    def max_dose(self, value):
        self._max_dose = value

    @property
    def rec_dose(self):
        return self._rec_dose

    @rec_dose.setter
    def rec_dose(self, value):
        self._rec_dose = value

    @property
    def min_time(self):
        return self._min_time

    @min_time.setter
    def min_time(self, value):
        self._min_time = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def cur_dose(self):
        return self._cur_dose

    @min_time.setter
    def cur_dose(self, value):
        self._cur_dose = value

    @property
    def last_time(self):
        return self._last_time

    @amount.setter
    def last_time(self, value):
        self._last_time = value
