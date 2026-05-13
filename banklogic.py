import sqlite3
import bcrypt
from database import Database
from classes import *

class CurrentSession:
    def create_new_user(self, new_profile):
        a = new_profile["adress"]
        adress_dict = Adress(
            street      = a["street"],
            post_number = a["post_number"],
            city        = a["city"],
            country     = a["country"]
            )
        new_user_profile = Persondetails(
            name          = new_profile["name"]
            person_number = new_profile["person_number"] #username
            email         = new_profile["email"]
            phonenumber   = new_profile["phonenumber"]
            adress        = adress_dict
            )
        # Create user with insert here.


    def create_account(self):
        pass
    
    def login(self):
        

        
        