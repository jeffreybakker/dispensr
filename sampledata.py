import database
from user import User
from prescription import Prescription
from inventory import Inventory

users = [
    User(1, 80, "pat", "", ""),
    User(2, 68465, "doc", "hoi", "wachtwoord")
]

prescriptions = [
    Prescription(1, 1, 2, "Tegen de hoofdpijn", 3, 5, 2, 0, 0, 0, 0, 0),
    Prescription(2, 1, 3, "Niet op kauwen", 4, 10, 1, 0, 0, 0, 0, 0),
    Prescription(3, 2, 1, "Tegen de hoofdpijn, oplossen in een bodempje water", 5, 2, 1, 0, 0, 0, 0, 0)
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
