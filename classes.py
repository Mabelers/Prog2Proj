from abc import ABC, abstractmethod
from valideringfunktioner import *

# Defines the base classes of accounts, adresses and usersprofiles.
class Account: 
    def __init__(self, account_number, person_number, balance, currency):
        self.account_number = account_number
        self.person_number = person_number
        self.balance = balance
        self.currency = currency

class Adress: 
    def __init__(self, street, post_number, city, country):
        self.street = street
        self.post_number = post_number
        self.city = city
        self.country = country

class Userprofile:
    def __init__(self, name, person_number, password,
                  email, phonenumber, adress: Adress):
        self.name = name
        self.person_number = person_number
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.adress = adress


        
        

# Defines the class transaction.
# Abstract subclass, demands each subsequent
# subclass to contain the method transaction type.
# This allows each transaction to be done through same method.
# Using different objects
class Transaction(ABC):
    def __init__(self, live_account: Account):
        self.live_account = live_account

    @abstractmethod
    def transaction_type(self):
        pass
    
# Deposit subclass:
# Allows for balance deposits to a loaded and selected account
class Deposit(Transaction):
    def transaction_type(self):
        print(f"\n\tYou have chosen to deposit",end=" ")
        print(f"balance into account {self.live_account.account_number}.\n")
        if not pathYesNo("Continue?"):
            return False
        print("\n\n\n\tPlease complete the following steps: ")
        print("\n\tWhat currency type are you depositing?")
        self.currencyfrom = currency_select()
        self.amount = balance_input("Deposit")

        # Same currency, simple addition
        if self.currencyfrom == self.live_account.currency:
            self.live_account.balance += self.amount
            return True
        else:
            # API call, fetches exchange rate for calculation 
            exchange_rate = currency_fetch(self.currencyfrom,self.live_account.currency)
            if not exchange_rate:
                print("\n\tOperation cannot complete due to current issue.")
                print("\tPlease try again later")
                input("\n\tPress enter to go back to account screen")
                return False
            
            # Updates the currently loaded accounts balance.
            real_amount = self.amount * exchange_rate
            self.live_account.balance += real_amount
            return True
            

# Withdraw subclass:
# Allows for withdrawals/removals of balance from selected and loaded account
class Withdraw(Transaction):
    def transaction_type(self):
        print(f"\n\tYou have chosen to withdraw",end=" ") 
        print(f"balance from account {self.live_account.account_number}.\n")
        if not pathYesNo("Continue?"):
            return False
        print("\n\n\n\tPlease complete the following steps: ")
        while True: 
            print("\n\tHow much and what currency type are you withdrawing?")

            # Currency / Amount inputs
            self.currencyfrom = currency_select()
            self.amount = balance_input("Withdrawal")

            # If currency type == identical, direct balance transfer
            if self.currencyfrom == self.live_account.currency:
                if self.live_account.balance < self.amount:
                    print(f"\n\tInsufficient balance!")
                    print(f"\n\tWithdrawal amount: {self.amount}!")
                    print(f"\tAccount balance {self.live_account.balance}!")
                    print("\n\t1. Back to accounts")
                    print("\t2. Insert new amount")
                    choice = pathChooseXnumber(2,"Your choice: ")
                    if choice == "1":
                        return False
                    elif choice == "2":
                        continue
                else:
                    self.live_account.balance -= self.amount
                    return True
                
            # if currency type != identical, call api to fetch exchange rate
            else:
                # API call, fetches exchange rate for calculation 
                exchange_rate = currency_fetch(self.currencyfrom,
                                               self.live_account.currency)
                if not exchange_rate:
                    print("\n\tOperation cannot complete due to an issue")
                    print("\tPlease try again later")
                    input("\n\tPress enter to go back to account screen")
                    return False
                
                # Updates the currently loaded accounts balance.
                real_amount = self.amount * exchange_rate
                if self.live_account.balance < real_amount:
                    print(f"\n\tInsufficient balance!")
                    print(f"\n\tWithdrawal amount: {real_amount}!")
                    print(f"\tAccount balance {self.live_account.balance}!")
                    print("\n\t1. Back to accounts")
                    print("\t2. Insert new amount")
                    choice = pathChooseXnumber(2,"Your choice: ")
                    if choice == "1":
                        return False
                    elif choice == "2":
                        continue
                self.live_account.balance -= real_amount
                return True

# Transfer subclass:
# Allows for transfer of balance between 2 accounts.
# param1: From: Current selected loaded account.
# param2: To: Second account loaded in main, 
#           right before this class and method is called.
#
class Transfer(Transaction):
    def __init__(self, live_account: Account, to_account: Account):
        super().__init__(live_account)
        self.to_account = to_account

    def transaction_type(self):
        print(f"\n\tYou have chosen to transfer balance:")
        print(f"\n\tFrom account number: {self.live_account.account_number}")
        print(f"\tTo account number: {self.to_account.account_number}\n\n")
        if not pathYesNo("Is this correct?"):
            return False
        print("\n\tPlease complete the following steps: ")
        while True: 
            print("\n\tHow much and what currency type are you transferring?")
            self.currencymiddleman = currency_select()
            self.amount = balance_input("Transfer")

            # Currency Match, direct transfer 
            # Variables to fix line lenght
            mid = self.currencymiddleman
            fromm = self.live_account.currency
            to = self.to_account.currency
            if mid == fromm == to:
                if self.live_account.balance < self.amount:
                    print(f"\n\tInsufficient balance!")
                    print(f"\n\tTransfer amount: {self.amount}!")
                    print(f"\tAccount balance {self.live_account.balance}!")
                    print("\n\t1. Back to accounts")
                    print("\t2. Insert new amount")
                    choice = pathChooseXnumber(2,"Your choice: ")
                    if choice == "1":
                        return False
                    elif choice == "2":
                        continue
                else:   
                        self.live_account.balance -= self.amount
                        self.to_account.balance += self.amount
                        return True
                # Currency mismatch. Involve API layer
            else:
                
                # Middle != From
                if self.currencymiddleman != self.live_account.currency:
                    # Fetches the exchange rate from accounts balance to 
                    # transfer currency balance.
                    exchange_from = currency_fetch(self.currencymiddleman,
                                                self.live_account.currency)
                    if not exchange_from:
                        print("\n\tOperation cannot complete due to an issue")
                        print("\tPlease try again later")
                        input("\n\tPress enter to go back to account screen")
                        return False
                    
                #Middle == From
                else:
                    exchange_from = 1

                # Midde != To
                if self.currencymiddleman != self.to_account.currency:
                    # Updates the currently loaded to_accounts balance.
                    exchange_rate_to = currency_fetch(self.currencymiddleman,
                                                    self.to_account.currency)
                    if not exchange_rate_to:
                        print("\n\tOperation cannot complete due to an issue")
                        print("\tPlease try again later")
                        input("\n\tPress enter to go back to account screen")
                        return False
                    
                # Middle == To
                else:
                    exchange_rate_to = 1

                # Sets a variable to the middle currency balance
                real_amount_middle = self.amount * exchange_from
                if self.live_account.balance < real_amount_middle:
                    print(f"\n\tInsufficient balance!")
                    print(f"\n\tTransfer amount(in ",end="")
                    print(f"{self.live_account.currency}): {real_amount_middle}!")
                    print(f"\tAccount balance {self.live_account.balance}!")
                    print("\n\t1. Back to accounts")
                    print("\t2. Insert new amount")
                    choice = pathChooseXnumber(2,"Your choice: ")
                    if choice == "1":
                        return False
                    elif choice == "2":
                        continue
                    
                real_amount_to = self.amount * exchange_rate_to
                self.live_account.balance -= real_amount_middle
                self.to_account.balance += real_amount_to
                return True

# ConvertCurrency subclass:
# Takes the currency type of the selected loaded account
# Allows user to change currency type, 
# Sses API to convert current balance to match new currency type.
class ConvertCurrency(Transaction):
    def transaction_type(self):
        while True:    
            print("\n\n\tYou have chosen to convert ",end="")
            print("your balance to a new currency type.")
            print("\n\tYour balance will be automatically",end="") 
            print(" updated to match the new currency.")
            input("\n\tPress ENTER to confirm")
            self.convertto = currency_select()
            if self.live_account.currency == self.convertto:
                print(f"\n\tYour account already uses ",end="")
                print(f"{self.live_account.currency}!")

                if pathYesNo("Cancel currency conversion?"):
                    return False
                else:
                    continue
            else:
                exchange_rate = currency_fetch(self.live_account.currency,
                                               self.convertto)
                if not exchange_rate:
                    print("\n\tOperation cannot complete due to an issue")
                    print("\tPlease try again later")
                    input("\n\tPress enter to go back to account screen")
                    return False

                new_balance = self.live_account.balance * exchange_rate
                self.live_account.balance = new_balance
                self.live_account.currency = self.convertto
                return True