import sqlite3


street = input("Gata")
postnmr = input("postnmr")
stad = input("stad")
land = input("land")

conn = sqlite3.connect("BankDatabase.db")
cursor = conn.cursor()

# 1. Insert address first
cursor.execute(
    "INSERT INTO Addresses (street, post_number, city, country) VALUES (?, ?, ?, ?)",
    (street, postnmr, stad, land)
)
address_id = cursor.lastrowid

# 2. Insert individual with that address_id
cursor.execute(
    "INSERT INTO Individuals (person_number, name, email, phonenumber, address_id) VALUES (?, ?, ?, ?, ?)",
    ("900101-1234", "Erik Karlsson", "erik@email.com", "0701234567", address_id)
)

conn.commit()
conn.close()
print("Test user created!")