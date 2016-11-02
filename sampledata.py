from user import User
from inventory import Inventory
from prescription import Prescription
import database

users = [
    User(1, 80, "pat", "", ""),
    User(2, 68465, "doc", "hoi", "wachtwoord")
]

prescriptions = [
    Prescription(1, 1, 2, "Niet voor inwendig gebruik", 3, 2, 5, 2, 0, 0, 0, 0, 0),
    Prescription(2, 1, 3, "Niet op kauwen", 4, 2, 10, 1, 0, 0, 0, 0, 0),
    Prescription(3, 2, 1, "Tegen de hoofdpijn", 5, 3, 2, 1, 0, 0, 0, 0, 0)
]

drugs = [
    Inventory(1, "Paracetamol", "liq", 500, 411),
    Inventory(2, "ANTIAIDS", "pil", 20, 14),
    Inventory(3, "Laxeermiddel", "liq", 50, 29)
]

database.init("data/database.db")

for user in users:
    database.insert_user(user)

for prescription in prescriptions:
    database.insert_prescription(prescription)

for drug in drugs:
    database.insert_inventory(drug)

database.commit()
