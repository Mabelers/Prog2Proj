from abc import ABC, abstractmethod
import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("BankDatabase.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
    
    def disconnect(self):
        self.connection.close()

    def savestate(self):
        self.connection.commit()


        

class AccountRepo:
    def __init__(self, database: Database):
        self.db = database

    def has_Account(self):
        pass
    def checkPerson_number(self, person_number):
        self.db.cursor.execute(
            "SELECT * FROM Individuals where person_number = ?", (person_number,)
            )
        row = self.db.cursor.fetchone()
        if has_Account(row):
            return 
        return
        
        

        



