import sqlite3
import bcrypt
from valideringfunktioner import *
from classes import Account, Persondetails, Adress

class Service:
    
    def __init__(self, database):
        self.db = database

    # Register new profile.

    def create_new_user(self):
        try:
            # Input validation function, outputs finished new account template.
            new_profile = create_person_input()
            print("New user template successfull.")
            print("Create a password to use on this profile!")

            # Password validation
            password = CreateValidPass()

            # Password hashing
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Create new user object
            a = new_profile["adress"]
            adress_obj = Adress(
                street      = a["street"],
                post_number = a["post_number"],
                city        = a["city"],
                country     = a["country"]
                )
            customer_data  = Persondetails(
                name          = new_profile["name"],
                person_number = new_profile["person_number"], #username
                password      = hashed_password,
                email         = new_profile["email"],
                phonenumber   = new_profile["phonenumber"],
                adress        = adress_obj
                )
            
            # SQLite database insert. Registers account to db officially
            # Then saves state of the new user with commit.

            address_id = self.db.db_insertAddress(adress_obj)
            self.db.db_insertCustomer(address_id,customer_data)
            self.db.savestate()
            return True    
        
        except sqlite3.IntegrityError:
            print("Your person number is already registered with our bank." \
            " Please log in")
            self.db.connection.rollback()
            return "login"
        except sqlite3.OperationalError:
            print("Database operational error")  
            self.db.connection.rollback()
            return False  
        except sqlite3.DatabaseError:  
            print("Database error")  
            self.db.connection.rollback()
            return False  
        except:
            print("Unknown error has crashed the user" \
            " creation enviroment. Contact the developer.")  
            self.db.connection.rollback()
            return False  
     
    
    def login(self):
        while True:
            # Validate login inputs
            person_config = VALIDATION_CONFIGURATIONS["person_number"]
            password_config = VALIDATION_CONFIGURATIONS["password"]
            person_number_input = multiValidationInput("person_number",person_config)
            password_input = multiValidationInput("password",password_config)
            
            # profile of personnumber
            login_profile = self.db.db_fetchIndividual(person_number_input)
            if not login_profile:
                print("Error, user not found.")
                continue
            # Compares password and users password hash, 
            # if match return true, otherwise false
            compare = bcrypt.checkpw(password_input.encode("utf-8"), 
                                        login_profile["passwordhash"])
            if compare == True:
                print(f"Password verified, Welcome {login_profile['name']}!")
                a = self.db.db_fetchAddress(login_profile["adress"])
                adress_obj = Adress(
                street      = a["street"],
                post_number = a["post_number"],
                city        = a["city"],
                country     = a["country"]
                )
                Current_User = Persondetails(
                name          = login_profile["name"],
                person_number = login_profile["person_number"], #username
                password      = login_profile["passwordhash"],
                email         = login_profile["email"],
                phonenumber   = login_profile["phonenumber"],
                adress        = adress_obj
                )
                return Current_User
            elif compare == False:
                print("Password mismatch, try again?")
                x = input("Y/N: ")
                if x.lower() == "y":
                    continue
                elif x.lower() == "n":
                    return False
            return False

    # Creates account, uses logged_in user to grab person_number,
    # creates a new account using that person_number as identifyer
    # Function to demand input for a currency, with a 
    # whitelist to decide allowed currencies.
    def create_new_account(self, loggedinUser):
        print(f"""Hello {loggedinUser.name}! Thank you for
               choosing to open a new account at Marcus bank system.""")

        currency = account_currency_select()

        account_id = self.db.db_insertAccount(loggedinUser, currency)

        print("Account creation successful!")
        print(f"A new account has been created with the '{loggedinUser.person_number}' identifier.")
        print(f"""
            New account details\n
            Account ID:\t {account_id}\n
            Belongs to:\t {loggedinUser.name}\n
            Currency type:\t {currency}\n""")

    
    def load_account(self, selected_account):
        live_account = Account(
        account_number  = selected_account["account_number"],
        person_number   = selected_account["person_number"], 
        balance         = selected_account["balance"],
        currency        = selected_account["currency"]
        )
        return live_account
    
        
        