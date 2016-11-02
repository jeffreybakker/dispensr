class Prescription:
    def __init__(self, id, uid, medicine_id, descr, max_dose, rec_dose, min_time, amount, cur_dose, last_time, pr_doctor, pr_date, dur_din, duration):
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
        self._doctor = pr_doctor
        self._date = pr_date
        self._dur_din = dur_din
        self._duration = duration

    @staticmethod
    def parse_raw(row):
        if row is None or len(row) != 14:
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
        tempprescription.doctor = row[10]
        tempprescription.date = row[11]
        tempprescription.dur_din = row[12]
        tempprescription.duration = row[13]
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

    @cur_dose.setter
    def cur_dose(self, value):
        self._cur_dose = value

    @property
    def last_time(self):
        return self._last_time

    @last_time.setter
    def last_time(self, value):
        self._last_time = value

    @property
    def doctor(self):
        return self._doctor

    @doctor.setter
    def doctor(self, value):
        self._doctor = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def dur_din(self):
        return self._dur_din

    @dur_din.setter
    def dur_din(self, value):
        self._dur_din = value

    @property
    def duration(self):
        return self._duraiton

    @duration.setter
    def duration(self, value):
        self._duration = value