import database
import calendar
import time


def add_new_user(user):
    """\
    Insert an <User> object into the database

    :param user: an object of the <User> type
    """
    database.insert_user(user)


def update_user(user):
    """\
    Updates the user entry in the database

    :param user: The <User> object that has to be updated in the database
    """
    database.update_user(user)


def get_user(rfid):
    """\
    Returns an <User> object for the user with the given RFID

    :param rfid: The ID of the RFID tag of the user
    :return: An <User> object for the given RFID, none if no user was found
    """
    return database.get_user_by_rfid(rfid)


def add_new_prescription(prescription):
    """\
    Inserts an <Prescription> object into the database

    :param prescription: An object of the <Prescription> type
    """
    database.insert_prescription(prescription)


def update_prescription(prescription):
    """\
    Updates the prescription entry in the database

    :param prescription: The <Prescription> object that has to be updated in the database
    """
    database.update_prescription(prescription)


def get_prescriptions(user):
    """\
    Returns a list of prescriptions that need to be handed out at that time to the given user

    :param user: An object of the <User> type
    :return: A list of prescriptions that need to be handed out at that time to the given user
    """
    prescriptions = user.get_prescriptions()

    # Create a list called res (result in the comments)
    # where all the prescriptions that need to be handed out will be stored in
    res = []

    # Select which prescriptions satisfy the condition and can therefore be added to the result list
    for pres in prescriptions:
        # If the minimum amount of time has not yet passed for the prescription, skip this one
        if pres.last_time + pres.min_time > calendar.timegm(time.gmtime()):
            continue

        # If the current dose is higher that or equal to the maximum dose, skip this one
        if pres.cur_dose >= pres.max_dose:
            continue

        # If the date the drug was prescribed and the duration the drug needs to be taken
        # are smaller than the current time, skip this one
        if pres.duration + pres.date < calendar.timegm(time.gmtime()):
            continue

        # If the amount of drug that needs to be handed out is higher than the current stock of that drug,
        # skip this one
        inventory = database.get_inventory_by_iid(pres.medicine_id)
        if inventory.stock < pres.amount:
            notify_inventory()
            continue

        # Set last_time to the current time
        pres.last_time = int(calendar.timegm(time.gmtime()))

        # Add 1 to the cur_dose
        pres.cur_dose += 1

        # Add the values to the prescription pres in the database
        database.update_prescription(pres)

        # Append the prescription pres to the result list
        res.append(pres)

    # Commits all database changes mad since the last commit
    database.commit()

    # Return the result list
    return res


def add_new_inventory(drug):
    """\
    Inserts an <Inventory> object into the database

    :param drug: An object of the <Inventory> type
    """
    database.insert_inventory(drug)


def update_inventory(drug):
    """\
    Update the inventory entry in the database

    :param drug: The <Inventory> object that has to be updated in the database
    """
    database.update_inventory(drug)


def get_inventory():
    """\
    Returns a list of all <Inventory objects in the database>

    :return: A list of <Inventory> objects
    """
    return database.get_inventory()


def get_drug_by_prescription(prescription):
    """\
    Returns the <Inventory> object for the given drug ID

    :param prescription: The drug ID
    :return: An <Inventory> object for the given drug ID
    """
    return database.get_inventory_by_iid(prescription.medicine_id)


def inventory_refill():
    """\
    Sets the stock of all drugs in the inventory to its maximum capacity
    """
    inventory = get_inventory()
    for i in inventory:
        i.stock = i.capacity
        database.update_inventory(i)

    database.commit()


def notify_inventory():
    pass  # TODO: add a notification
