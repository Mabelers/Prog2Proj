import sqlite3
import bcrypt
from database import *
from valideringfunktioner import *
from classes import *

class Service:
    
    def __init__(self, database: Customers):
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

            address_id = self.db.db_insertAdress(adress_obj)
            self.db.db_insertCustomer(address_id,customer_data)
        except sqlite3.IntegrityError:
            print("Your person number is already registered with our bank." \
            " Please log in")
            return "login"
        except sqlite3.OperationalError:
            print("Database operational error")  
            return False  
        except sqlite3.DatabaseError:  
            print("Database error")  
            return False  
        except:
            print("Unknown error has crashed the user" \
            " creation enviroment. Contact the developer.")  
            return False  
        return True    
        


    def create_account(self):
        pass
    
    def login(self):
        while True:
            # Validate login inputs
            person_config = VALIDATION_CONFIGURATIONS["person_number"]
            password_config = VALIDATION_CONFIGURATIONS["password"]
            person_number_input = multiValidationInput("person_number",person_config)
            password_input = multiValidationInput("password",password_config)
            
            # profile of personnumber
            login_profile = self.db.db_fetchIndividual(person_number_input)

            # Compares password and users password hash, 
            # if match return true, otherwise false
            compare = bcrypt.checkpw(password_input.encode("utf-8"), 
                                        login_profile["passwordhash"])
            if compare == True:
                print(f"Password verified, Welcome {login_profile["name"]}!")
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
                password      = login_profile["hashedpw"],
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


            

        
        