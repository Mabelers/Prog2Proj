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
        except KeyboardInterrupt:
            exit()
        except:
            print("Unknown error has crashed the user" \
            " creation enviroment. Contact the developer. ")  
            self.db.connection.rollback()
            return False  
     
    
    def login(self):
        while True:
            # Validate login inputs
            person_config = VALIDATION_CONFIGURATIONS["person_number"]
            password_config = VALIDATE_PASSWORD["password"]

            person_number_input = multiValidationInput("person_number",person_config)
            if person_number_input == False:
                return False
            password_input = multiValidationInput("password",password_config)
            
            # profile of personnumber
            login_profile = self.db.db_fetchIndividual(person_number_input)
            if not login_profile:
                print("\n\tWe could not find this user registered.")
                print("\n\tMake sure your information is correct.\n")
                if pathYesNo("Try again?"):
                    continue
                else: 
                    return False
            # Compares password and users password hash, 
            # if match return true, otherwise false
            compare = bcrypt.checkpw(password_input.encode("utf-8"), 
                                        login_profile["passwordhash"])
            if compare == True:
                print(f"\n\tPassword verified.")
                print(f"\n\n\n\tWelcome {login_profile['name']}!")
                a = self.db.db_fetchAddress(login_profile["address_id"])
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
                print("\n\tPassword mismatch, try again?")
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
        print(f"""\n\tHello {loggedinUser.name}! 
        Thank you for choosing to open a new account at Marcus bank system.\n""")

        print("""\tSelect a currency type for your account.

        This will be the currency type for your entire balance tied to this account.
        This can be changed at a later date!""")
        currency = currency_select()
        print("\n\tConfirm account details: ")
        print(f"\tNameholder: {loggedinUser.name}")
        print(f"\tPerson number: {loggedinUser.person_number}")
        print(f"\tCurrency type: {currency}")
        print(f"\tInitial Balance: 0 {currency}\n")
        if pathYesNo("Create this account?"):  
            account_id = self.db.db_insertAccount(loggedinUser, currency)
        else:
            return False

        print("\n\n\tAccount creation successful!")
        print(f"\tA new account has been created from unique user '{loggedinUser.person_number}'!")
        print(f"""
            New account details:\n
            Account ID: {account_id}\n
            Belongs to: {loggedinUser.name}\n
            Currency type: {currency}\n""")

    
    def load_account(self, selected_account):
        live_account = Account(
        account_number  = selected_account["account_number"],
        person_number   = selected_account["person_number"], 
        balance         = selected_account["balance"],
        currency        = selected_account["currency"]
        )
        return live_account
    
        
        