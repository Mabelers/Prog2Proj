from abc import ABC, abstractmethod
import sqlite3


class Database:
    def Connect(self):
        self.connect = sqlite3.connect("BankDatabase.db")
        self.cursor = self.connect.cursor()
    
    def Disconnect(self):
        self.connect.close()

    def Savestate(self):
        self.connect.commit()


class Saved_Accounts(ABC):
    def __init__(self, database: Database):
        self.database = database

