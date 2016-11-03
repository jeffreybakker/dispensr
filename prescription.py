import json


class Prescription:
    def __init__(self, id=0, uid=0, medicine_id=0, descr='', max_dose=0, min_time=0, amount=0, cur_dose=0, last_time=0,
                 pr_doctor=0, pr_date=0, duration=0):
        self._id = id
        self._uid = uid
        self._medicine_id = medicine_id
        self._descr = descr
        self._max_dose = max_dose
        self._min_time = min_time
        self._amount = amount
        self._cur_dose = cur_dose
        self._last_time = last_time
        self._doctor = pr_doctor
        self._date = pr_date
        self._duration = duration

    @staticmethod
    def parse_raw(row):
        if row is None: # or len(row) != 12:
            return None

        tempprescription = Prescription()
        tempprescription.id = row[0]
        tempprescription.uid = row[1]
        tempprescription.medicine_id = row[2]
        tempprescription.descr = row[3]
        tempprescription.max_dose = row[4]
        tempprescription.min_time = row[5]
        tempprescription.amount = row[6]
        tempprescription.cur_dose = row[7]
        tempprescription.last_time = row[8]
        tempprescription.doctor = row[9]
        tempprescription.date = row[10]
        tempprescription.duration = row[11]
        return tempprescription

    @staticmethod
    def to_json(pres):
        if not pres:
            return None

        data = {}
        data["id"] = pres.id
        data["uid"] = pres.uid
        data["medicine_id"] = pres.medicine_id
        data["descr"] = pres.descr
        data["max_dose"] = pres.max_dose
        data["min_time"] = pres.min_time
        data["amount"] = pres.amount
        data["cur_dose"] = pres.cur_dose
        data["last_time"] = pres.last_time
        data["doctor"] = pres.doctor
        data["date"] = pres.date
        data["duration"] = pres.duration

        return json.dumps(data)

    @staticmethod
    def to_json_list(prescriptions):
        data = {}
        for i in range(0, len(prescriptions)):
            data[i] = Prescription.to_json(prescriptions[i])

        return json.dumps(data)

    @staticmethod
    def from_json_list(json_datas):
        print("json_datas: " + str(json_datas))
        datas = json.loads(json_datas)
        prescriptions = {}

        for i in range(0, len(datas)):
            prescriptions[i] = Prescription.from_json(datas[str(i)])
            print("prescription: " + str(prescriptions[i]))

        return prescriptions

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)

        pres = Prescription()
        pres.id = data["id"]
        pres.uid = data["uid"]
        pres.medicine_id = data["medicine_id"]
        pres.descr = data["descr"]
        pres.max_dose = data["max_dose"]
        pres.min_time = data["min_time"]
        pres.amount = data["amount"]
        pres.cur_dose = data["cur_dose"]
        pres.last_time = data["last_time"]
        pres.doctor = data["doctor"]
        pres.date = data["date"]
        pres.duration = data["duration"]

        return pres

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
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
