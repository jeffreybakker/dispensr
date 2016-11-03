def init():
    import calendar

    import time

    import database
    from user import User
    from prescription import Prescription
    from inventory import Inventory


# id, rfid, role(pat, doc, ref), username, password
    users = [
        User(1, 80, "pat", "", ""),
        User(2, 68465, "doc", "c.s.jansen", "qwerty"),
        User(3, 586812701, "pat", "", ""),
        User(4, 3621006848, "pat", "", ""),
        User(5, test, "ref", "", ""),
        User(6, test, "pat", "", ""),
        User(7, test, "pat", "", ""),
        User(8, test, "doc", "u.aarts", "noscopez"),
        User(9, test, "pat", "", ""),
        User(10, test, "pat", "", "")
    ]

# id, uid(id_patient), medicine_id, desc, max_dose, min_time, amount, cur_dose, last_time, doctor(id_doctor), date, duration
    prescriptions = [
        Prescription(1, 3, 2, "Tegen de hoofdpijn", 3, 5, 2, 0, 0, 0, calendar.timegm(time.gmtime()), 53135135130),
        Prescription(2, 4, 3, "Niet op kauwen", 4, 10, 1, 0, 0, 0, calendar.timegm(time.gmtime()), 6843515430),
        Prescription(3, 2, 1, "Tegen de hoofdpijn, oplossen in een bodempje water", 5, 2, 1, 0, 0, 0, calendar.timegm(time.gmtime()), 45413516840)
    ]

# id, name, type, capacity, stock
    drugs = [
        Inventory(1, "Paracetamol", "sol", 500, 411),
        Inventory(2, "Hoestdrank", "liq", 500, 414),
        Inventory(3, "Asperine", "pil", 500, 429)
    ]

    database.init("data/database.db", True)

    for user in users:
        database.insert_user(user)

    for prescription in prescriptions:
        database.insert_prescription(prescription)

    for drug in drugs:
        database.insert_inventory(drug)

    database.commit()
