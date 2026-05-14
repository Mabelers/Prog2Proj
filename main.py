from banklogic import Service
from classes import *
from database import Customers
from valideringfunktioner import account_select, transfer_account_input

# REMINDER ADD COMMIT AND DISCONNECT BEFORE TESTING.

# Main loop for whole program, allows for seamless
# logout to login to new user.
while True:
    
    # Loop for login/registration
    while True:
        print("Welcome to Marcus banking system")
        print("Choose one of following options: \n\n")
        print("1. Login to bank")
        print("2. Register with us")
        print("3. Exit system")


        # Decide program path
        choose = input("1/2/3 Your Choice: ")

        # Start initial object, connects to database.
        db = Customers()
        session = Service(db)

        # Login option, requires previous registration
        if choose == "1":
            logged_in = session.login()
            if logged_in == True:
                pass
            else:
                continue
            break
            
        # Registration option. Adds user to DB.
        elif choose == "2":
            print("""
                You have chosen to register at our bank.\n
                You will now be guided through the registration process.
                """)
            
            # Creates new user,
            result = session.create_new_user()
            if result == False:
                print("""An error has occured in the program, 
                    currently we dont support these bugs, 
                    program will now shutdown.""")
                
            elif result == "login":
                logged_in = session.login()
                if logged_in == True:
                    pass
                else:
                    continue
                break
            
            elif result == True:
                print("Registration complete.")
        
        # Exits program, 
        elif choose == "3":
            print("Exiting bank system, have a good day!")
            exit()

    # Loop for account selection / account creation.
    while True:
        print(f"Welcome {logged_in.name}!")
        accounts = session.db.db_fetchAccounts(logged_in.person_number)
        if not accounts:
            print(f"""It appears you do not have an account registered with 
                  us yet.\n Please create a new account to start banking with us.""")
            session.create_new_account(logged_in)
            
        else:
            print("Your accounts:")
            n = 1
            for account in accounts:
                print("\n\n-----------------------------------\n\n")
                print(f"\t\tAccount {n}:\n\n")
                print("\n-----------------------------------\n")
                print(f"Account number: {account["account_number"]}\n")
                print(f"Account balance: {account["balance"]:.2f} {account["currency"]}\n")
                print(f"Account user: {account["person_number"]}\n")
                print("\n\n-----------------------------------\n\n")
                n += 1

        print("Pick one of your accounts to access.")
        user_accounts = []
        for account in accounts:
            print(f"\t{account["account_number"]}\n")
            user_accounts.append(account["account_number"])
        selected_id = account_select(user_accounts)
        selected_account = session.db.db_selectAccount(selected_id)
        live_account = session.load_account(selected_account)
        while True:
            print("Account selected")
            print("What do you want to do with this account?")
            print("1. Withdrawal")
            print("2. Deposit")
            print("3. Transfer")
            print(f"4. Change currency type: Current ['{live_account.currency}'.]")

            # Small whitelist of options going forward in program
            allowed = {"1","2","3","4"}

            option = input("Select option 1-4: ")
            # Iterate through these options
            while option not in allowed:
                print("Not an option.")
                option = input("Select option 1-4: ")

            # Account balance Withdrawal
            if option == "1":


                withdraw = Withdraw(live_account)
                op_result = withdraw.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                else:
                    print("Withdrawal failed. Choose another option.")
                    continue



            # Account balance Deposit
            elif option == "2":
                
                deposit = Deposit(live_account)
                op_result = deposit.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                else:
                    print("Deposit failed. Choose another option.")
                    continue
            

            # Account balance Transfer
            elif option == "3":
                transfer_id = transfer_account_input()
                transfer_account = session.db.db_selectAccount(transfer_id)
                to_account = session.load_account(transfer_account)
                transfer = Transfer(live_account, to_account)

                op_result = transfer.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    session.db.db_save_Account(to_account)
                else:
                    print("Transfer failed. Choose another option.")
                    continue
                
            # Account currency Converter
            elif option == "4":
                pass
        
            
            
            

            
