import sqlite3

connection = sqlite3.connect("BankDatabase.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT * FROM Individuals WHERE address_id = ?", (1,))
row = cursor.fetchone()
print(dict(row))

name = row["name"]
email = row["email"]
phonenumber = row["phonenumber"]
person_number = row["person_number"]
ides = row["id"]

new = input("ny mail")
cursor.execute("UPDATE Individuals SET email = ? WHERE id = ?",
                (new, ides))

connection.commit()

cursor.execute("SELECT * FROM Individuals WHERE address_id = ?", (1,))
row = cursor.fetchone()


print(dict(row))


connection.close()

