def init():
    """/
    Insert all the sample data into the database
    """
    import calendar
    import time
    import database
    from user import User
    from prescription import Prescription
    from inventory import Inventory

    # User class contains: id, rfid, role(pat, doc, ref), username, password
    users = [
        User(1, 2654408544, "pat", "", ""),  # Lars student card
        User(2, 3519617066, "doc", "c.s.jansen", "qwerty"),  # Martijn OV - chip card personal
        User(3, 586812701, "pat", "", ""),  # Blank pass
        User(4, 3621006848, "pat", "", ""),  # Blue keychain
        User(5, 3690740861, "ref", "", ""),  # Lars schoolpass 2015-2016
        User(6, 2204658921, "pat", "", ""),  # Lars schoolpass 2014-2015
        User(7, 2932035940, "pat", "", ""),  # Frank student card
        User(8, 2844322267, "doc", "u.aarts", "noscopez"),  # Frank OV - Chip card anonymous
        User(9, 243991904, "pat", "", ""),  # Arwin student card
        User(10, 3254740226, "pat", "", "")  # Arwin OV - chip card personal
    ]

    # Prescription class contains: id, uid(id_patient), medicine_id, desc, max_dose, min_time, amount, cur_dose,
    # last_time, doctor(id_doctor), date, duration
    prescriptions = [
        Prescription(1, 3, 2, "Tegen de hoofdpijn", 3, 5, 2, 0, 0, 0, calendar.timegm(time.gmtime()), 53135135130),
        Prescription(2, 4, 3, "Niet op kauwen", 4, 10, 1, 0, 0, 0, calendar.timegm(time.gmtime()), 6843515430),
        Prescription(3, 2, 1, "Tegen de hoofdpijn, oplossen in een bodempje water", 5, 2, 1, 0, 0, 0,
                     calendar.timegm(time.gmtime()), 45413516840)
    ]

    # Inventory class contains: id, name, type, capacity, stock
    drugs = [
        Inventory(1, "Paracetamol", "sol", 500, 411),
        Inventory(2, "Hoestdrank", "liq", 500, 414),
        Inventory(3, "Asperine", "pil", 500, 429),
        Inventory(4, "Kinzalkomb", "pil", 500, 486),
        Inventory(5, "Xatral", "liq", 500, 435),
        Inventory(6, "Stromectol", "liq", 500, 411),
        Inventory(7, "Beryx", "sol", 500, 489),
        Inventory(8, "Niaspan", "liq", 500, 477),
        Inventory(9, "Norgestimaat", "pil", 500, 305),
        Inventory(10, "Venlafaxine", "pil", 500, 458),
        Inventory(11, "Visanne", "sol", 500, 479)
    ]

    database.init("data/database.db", True)

    # Insert all the users in users into the database
    for user in users:
        database.insert_user(user)

    # Insert all prescriptions in prescriptions into the database
    for prescription in prescriptions:
        database.insert_prescription(prescription)

    # Insert all drugs in drugs into the database
    for drug in drugs:
        database.insert_inventory(drug)

    # Commits all database changes mad since the last commit
    database.commit()
