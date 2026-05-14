import sqlite3
from classes import Account


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("BankDatabase.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        self.connection.close()

    def savestate(self):
        self.connection.commit()


        

class Customers(Database):

    def db_insertAddress(self, adress_obj):
        self.cursor.execute(
        "INSERT INTO Addresses (street, post_number, city, country) VALUES (?, ?, ?, ?)",
        (adress_obj.street, adress_obj.post_number, adress_obj.city, adress_obj.country)
        )
        return self.cursor.lastrowid

    def db_insertCustomer(self, address_id, customer_data):
        self.cursor.execute(
        """
        INSERT INTO Individuals 
        (person_number, name, email, phonenumber, address_id, passwordhash) 
        VALUES 
        (?, ?, ?, ?, ?, ?)""",
        (customer_data.person_number,
        customer_data.name,
        customer_data.email,
        customer_data.phonenumber,
        address_id,
        customer_data.password)
            )
        
    def db_insertAccount(self, loggedinUser, currency):
        self.cursor.execute("""
        INSERT INTO Accounts
        (person_number, balance, currency)
        VALUES
        (?, ?, ?)""",
        (loggedinUser.person_number, 0, currency)
        )
        self.savestate()
        return self.cursor.lastrowid
    

    def db_fetchIndividual(self, person_number_input):
        self.cursor.execute(
            "SELECT * FROM Individuals WHERE person_number = ?",
            (person_number_input, )
            )
        return self.cursor.fetchone()
        
    def db_fetchAddress(self, person_number_input):
        self.cursor.execute(
            "SELECT * FROM Addresses WHERE person_number = ?",
            (person_number_input, )
            )
        return self.cursor.fetchone()
        
    def db_fetchAccounts(self, person_number):
        self.cursor.execute(
            "SELECT * FROM Accounts WHERE person_number = ?",
            (person_number, )
            )
        return self.cursor.fetchall()
    
    def db_selectAccount(self, account_number):
        self.cursor.execute(
            "SELECT * FROM Accounts WHERE account_number = ?",
            (account_number, )
            )
        return self.cursor.fetchone()
        
    def db_save_Account(self, account: Account):
        self.cursor.execute(
            """
            UPDATE Accounts 
            SET balance = ?, currency = ? 
            WHERE account_number = ?
            """, 
            (account.balance, account.currency, account.account_number))
        self.savestate()


    # def checkPerson_number(self, person_number):
    #     self.cursor.execute(
    #         "SELECT * FROM Individuals where person_number = ?", (person_number,)
    #         )
    #     row = self.cursor.fetchone()
    #      Add check for account, compare with person number
        
        

        



