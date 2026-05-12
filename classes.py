from abc import ABC, abstractmethod
from accountsdb import Database

class Account: 
    def __init__(self, balance, accountdetails: Accountdetails ):
        self.balance = balance
        self.accountdetails = accountdetails

class Persondetails:
    def __init__(self, name, person_number, email, phonenumber, adress: Adress):
        self.name = name
        self.person_number = person_number
        self.email = email
        self.phonenumber = phonenumber
        self.adress = adress

class Adress: 
    def __init__(self, street, post_number, city, country):
        self.street = street
        self.post_number = post_number
        self.city = city
        self.country = country

class Transaction(ABC):
    def __init__(self, amount, my_account: Account):
        self.amount = amount
        self.my_account = my_account

    @abstractmethod
    def transaction_type(self):
        pass
    
class Deposit(Transaction):
    def transaction_type(self):
       self.my_account.balance += self.amount

class Withdraw(Transaction):
    def transaction_type(self):
       self.my_account.balance -= self.amount
    

class Transfer(Transaction):
    def transaction_type(self, to_account):
        if self.my_account.balance < self.amount:
            print("NOT ENOUGH BALANCE")
        self.my_account.balance -= self.amount
        to_account.saldo += self.amount
        

        



