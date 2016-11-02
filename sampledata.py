import database
from user import User
from prescription import Prescription
from inventory import Inventory

users = [
    User(1, 80, "pat", "", ""),
    User(2, 68465, "doc", "hoi", "wachtwoord"),
    User(3, 586812701, "pat", "", ""),
    User(4, 3621006848, "pat", "", "")
]

prescriptions = [
    Prescription(1, 3, 2, "Tegen de hoofdpijn", 3, 2, 5, 2, 0, 0, 0, 0, 0),
    Prescription(2, 4, 3, "Niet op kauwen", 4, 2, 10, 1, 0, 0, 0, 0, 0),
    Prescription(3, 1, 1, "Tegen de hoofdpijn, oplossen in een bodempje water", 5, 3, 2, 1, 0, 0, 0, 0, 0)
]

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
