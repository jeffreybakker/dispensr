import database
import calendar
import time


def add_new_user(user):
    database.insert_user(user)


def update_user(user):
    database.update_user(user)


def get_user(rfid):
    return database.get_user_by_rfid(rfid)


def add_new_prescription(prescription):
    database.insert_prescription(prescription)


def update_prescription(prescription):
    database.update_prescription(prescription)


def get_prescriptions(user):
    prescriptions = user.get_prescriptions()

    print(prescriptions)

    res = []

    for pres in prescriptions:
        # If the minimum amount of time has not yet passed for the prescription, skip this one
        print('oi', calendar.timegm(time.gmtime()), pres.last_time + pres.min_time)
        if pres.last_time + pres.min_time > calendar.timegm(time.gmtime()):
            continue

        print('oi m8')
        if pres.cur_dose > pres.max_dose:
            continue

        print('oi m8, u wot?', pres.duration + pres.date, calendar.timegm(time.gmtime()))
        if pres.duration + pres.date < calendar.timegm(time.gmtime()):
            continue

        print('oi m8, u wot, get shrekt')
        inventory = database.get_inventory_by_iid(pres.medicine_id)
        if inventory.stock < pres.amount:
            notify_inventory()
            continue

        print('ok den')
        pres.last_time = int(calendar.timegm(time.gmtime()))
        pres.cur_dose += 1

        database.update_prescription(pres)

        res.append(pres)

    database.commit()

    print('je moedyr')
    return res


def add_new_inventory(drug):
    database.insert_inventory(drug)


def update_inventory(drug):
    database.update_inventory(drug)


def get_inventory():
    return database.get_inventory()


def get_drug_by_prescripiton(prescription):
    return database.get_inventory_by_iid(prescription.medicine_id)


def inventory_refill():
    inventory = get_inventory()

    for i in inventory:
        i.stock = i.capacity
        database.update_inventory(i)

    database.commit()


def notify_inventory():
    pass
