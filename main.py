from database import *
from banklogic import *
from classes import *

while True:
    print("Welcome to Marcus banking system")
    print("Choose one of following options: \n\n")
    print("1. Login to bank")
    print("2. Register with us")
    print("3. Exit system")

    choose = input("1/2/3 Your Choice: ")
    session = Service()

    if choose == "1":
        if session.login():
            pass
        else:
            continue
    elif choose == "2":
        print("""
              You have chosen to register at our bank.\n
              You will now be guided through the registration process.
              """)
        
        result = session.create_new_user()
        if result == False:
            print("""An error has occured in the program, 
                  currently we dont support these bugs, 
                  program will now shutdown.""")
        elif result == "login":
            # Login logic
            pass
        elif result == True:
            print("Registration complete.")
            
    elif choose == "3":
        break