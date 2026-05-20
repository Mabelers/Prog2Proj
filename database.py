import sqlite3
from classes import Account


# Class Database:
# Starts a connection with the database, 
# contains commit, connect and close methods.
class Database:
    

    def __init__(self):
        try:
            self.connection = sqlite3.connect("BankDatabase.db")
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("\n\tError connecting to database: ", e)
            print("\tFatal program error, no database = no program.\n\tBye!")

    def disconnect(self):
        self.connection.close()

    def savestate(self):
        self.connection.commit()


        
# Class DBoperations(Database): Database subclass.
# Contains pure database methods, inserts, selects, update.
# Called by banklogic, to conduct actions related to database.
class DBoperations(Database):

    # Inserts a new address object to the db
    def db_insertAddress(self, adress_obj):
        self.cursor.execute(
        """INSERT INTO Addresses
        (street, post_number, city, country) VALUES (?, ?, ?, ?)""",
        (adress_obj.street, adress_obj.post_number,
        adress_obj.city, adress_obj.country)
        )
        return self.cursor.lastrowid

    # Inserts a new user/individual object to the db
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
    
    # Inserts a new account to the db, using user personnumber as reference
    def db_insertAccount(self, loggedinUser, currency):
        self.cursor.execute("""
        INSERT INTO Accounts
        (person_number, balance, currency)
        VALUES
        (?, ?, ?)""",
        (loggedinUser.person_number, 0, currency)
        )
        return self.cursor.lastrowid
    

    # Fetches a user registered to the db
    def db_fetchIndividual(self, person_number_input):
        self.cursor.execute(
            "SELECT * FROM Individuals WHERE person_number = ?",
            (person_number_input, )
            )
        return self.cursor.fetchone()
    
    # Fetches an adress registered to the db
    def db_fetchAddress(self, address_id):
        self.cursor.execute(
            "SELECT * FROM Addresses WHERE id = ?",
            (address_id, )
            )
        return self.cursor.fetchone()
    
    # Fetches all accounts related to the users person_number
    def db_fetchAccounts(self, person_number):
        self.cursor.execute(
            "SELECT * FROM Accounts WHERE person_number = ?",
            (person_number, )
            )
        return self.cursor.fetchall()
    
    # Fetches a single account, using the unique account_number
    def db_selectAccount(self, account_number):
        self.cursor.execute(
            "SELECT * FROM Accounts WHERE account_number = ?",
            (account_number, )
            )
        return self.cursor.fetchone()
    
    # Updates and saves the state of an account, used for Account actions
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
        
        

        



