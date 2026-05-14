from abc import ABC, abstractmethod
from valideringfunktioner import currency_fetch,balance_input,currency_select

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

class Persondetails:
    def __init__(self, name, person_number, password, email, phonenumber, adress: Adress):
        self.name = name
        self.person_number = person_number
        self.password = password
        self.email = email
        self.phonenumber = phonenumber
        self.adress = adress


        
        


class Transaction(ABC):
    def __init__(self, live_account: Account):
        self.live_account = live_account

    @abstractmethod
    def transaction_type(self):
        pass
    
class Deposit(Transaction):
    def transaction_type(self):
        print(f"You have chosen to deposit balance into account {self.live_account.account_number}.")
        input("Press enter to continue")
        print("Please complete the following steps: ")
        print("What currency type are you depositing?")
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
                print("""Operation cannot complete due to current issue. 
                      \nPlease try again later""")
                input("Press enter to go back to account screen")
                return False
            
            # Updates the currently loaded accounts balance.
            real_amount = self.amount * exchange_rate
            self.live_account.balance += real_amount
            return True
            


class Withdraw(Transaction):
    def transaction_type(self):
        print(f"You have chosen to withdraw balance from account {self.live_account.account_number}.")
        input("Press enter to continue")
        print("Please complete the following steps: ")
        while True: 
            print("How much and what currency type are you withdrawing?")
            self.currencyfrom = currency_select()
            self.amount = balance_input("Withdrawal")

            # Same currency, simple subtraction
            if self.currencyfrom == self.live_account.currency:
                if self.live_account.balance < self.amount:
                    print(f"Insufficient balance!")
                    print(f"Withdrawal amount: {self.amount}!")
                    print(f"Account balance {self.live_account.balance}!")
                    continue
                else:
                    self.live_account.balance -= self.amount
                    return True
            else:
                # API call, fetches exchange rate for calculation 
                exchange_rate = currency_fetch(self.currencyfrom,self.live_account.currency)
                if not exchange_rate:
                    print("""Operation cannot complete due to current issue. 
                        \nPlease try again later""")
                    input("Press enter to go back to account screen")
                    return False
                
                # Updates the currently loaded accounts balance.
                real_amount = self.amount * exchange_rate
                if self.live_account.balance < real_amount:
                    print(f"Insufficient balance!")
                    print(f"Withdrawal amount: {real_amount}!")
                    print(f"Account balance {self.live_account.balance}!")
                    continue
                self.live_account.balance -= real_amount
                return True

class Transfer(Transaction):
    def __init__(self, live_account: Account, to_account: Account):
        super().__init__(live_account)
        self.to_account = to_account

    def transaction_type(self):
        print(f"""You have chosen to transfer balance: \n
            From account: {self.live_account.account_number}\n
            To account: {self.to_account.account_number}\n\n""")
        input("Press enter to continue")
        print("Please complete the following steps: ")
        while True: 
            print("How much and what currency type are you transferring?")
            self.currencymiddleman = currency_select()
            self.amount = balance_input("Transfer")

             # Same currency, simple subtraction
            if self.currencymiddleman == self.live_account.currency == self.to_account.currency:
                if self.live_account.balance < self.amount:
                    print(f"Insufficient balance!")
                    print(f"Transfer amount: {self.amount}!")
                    print(f"Account balance {self.live_account.balance}!")
                    print("Type 'cancel' to cancel transaction!")
                    x = input("If you want to input a new amount, simply press enter.")
                    if x.lower() == "cancel":
                        return False
                    continue
                else:   
                        self.live_account.balance -= self.amount
                        self.to_account.balance += self.amount
                        return True
            else:

                # API CALL:
                # Fetches the exchange rate from accounts balance to transfer currency balance.
                exchange_from = currency_fetch(self.currencymiddleman,self.live_account.currency)
                if not exchange_from:
                    print("""Operation cannot complete due to current issue. 
                        \nPlease try again later""")
                    input("Press enter to go back to account screen")
                    return False
                
                # Updates the currently loaded to_accounts balance.
                exchange_rate_to = currency_fetch(self.currencymiddleman,self.to_account.currency)
                if not exchange_rate_to:
                    print("""Operation cannot complete due to current issue. 
                        \nPlease try again later""")
                    input("Press enter to go back to account screen")
                    return False
                
                # Sets a variable to the middle currency balance
                real_amount_middle = self.amount * exchange_from
                if self.live_account.balance < real_amount_middle:
                    print(f"Insufficient balance!")
                    print(f"Transfer amount: {real_amount_middle}!")
                    print(f"Account balance {self.live_account.balance}!")
                    continue
                
                real_amount_to = self.amount * exchange_rate_to
                self.live_account.balance -= real_amount_middle
                self.to_account.balance += real_amount_to
                return True
        
class ConvertCurrency(Transaction):
    def transaction_type(self):
        while True:    
            print("You have chosen to convert your balance to a new currency type.")
            print("Your balance will be automatically updated to match the new currency.")
            input("Press enter to continue")
            self.convertto = currency_select()
            if self.live_account.currency == self.convertto:
                print(f"Your account already uses {self.live_account.currency}!")
                print("Select a new currency? Or cancel currency conversion?")
                print("Press enter to continue \nType 'cancel' and enter to cancel'")
                x = input("ENTER/'cancel'")
                if x.lower() == "cancel":
                    return False
                else:
                    continue
            else:
                exchange_rate = currency_fetch(self.live_account.currency,self.convertto)
                if not exchange_rate:
                    print("""Operation cannot complete due to current issue. 
                        \nPlease try again later""")
                    input("Press enter to go back to account screen")
                    return False

                new_balance = self.live_account.balance * exchange_rate
                self.live_account.balance = new_balance
                self.live_account.currency = self.convertto
                return True
        



