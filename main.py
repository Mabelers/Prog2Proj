from banklogic import Service
from time import sleep
from classes import *
from database import DBoperations
from valideringfunktioner import *  
# Banking system program, allows user to register as a user.
# And then also allows that user to make seperate accounts.
# Accounts can Deposit, Withdraw, Transfer and Convert their currency type.


# Program start, main loop start.
while True:
    
    # Program introduction, login/registration loop start.
    while True:
        print("\n\tWelcome to Marcus banking system")
        print("\tChoose one of following options: \n")
        print("\t1. Login to bank")
        print("\t2. Register with us")
        print("\t3. Exit system\n")


        # Decide program path
        choose = pathChooseXnumber(3,"Select option 1-3: " )

        # Starts session, by creating a Service() object.
        # Uses the Database subclass DBoperations(), using composition.
        # To add a database connection into the main session.
        db = DBoperations()
        session = Service(db)

        # Login Path. Demands previous registration
        if choose == "1":
            print("")
            logged_in = session.login()
            if not logged_in:
                continue
            break
            
        # Registration Path. Adds a new user registration.
        elif choose == "2":
            print("\n\tYou have chosen to register at our bank.")
            print("\tYou will now be guided",end="")
            print(" through the registration process.")

            result = session.create_new_user()

            # Registration failed Path, program shutdown.
            if result == False:
                print("\n\tAn error has occured in the program.")
                print("\tCurrently we dont support these bugs, ",end="")
                print("program will now shutdown.")
                exit()
            # Secondary login Path, if user already exists
            elif result == "login":
                logged_in = session.login()
                
                if not logged_in:
                    continue
                break
                
            # Registration complete, restarts login loop.
            elif result == True:
                print("\tRegistration complete.")
        
        # Exits program, 
        elif choose == "3":
            print("Exiting bank system, have a good day!")
            exit()

    # Loop for account selection / account creation.
    while True:
        print("\n\tWhat are we doing today?\n")
        print("\t1. Select an existing account")
        print("\t2. Create new account")
        print("\t3. Logout from bank\n")
        # Account Path: Decide to select/create/logout from user
        account_path = pathChooseXnumber(3,"Select option 1-3: ")

        # Select Path, Fetches all accounts tied to the logged in user.
        if account_path == "1":
            accounts = session.db.db_fetchAccounts(logged_in.person_number)

            # If no accounts on attempt select, allows for creation of new.
            if not accounts:
                print("\n\tIt appears you do not ",end="")
                print("have an account registered with us yet.")
                print("\n\tDo you want to create an account?",end="")
                print(" To use our bank you have to.")
                if pathYesNo("Create account?"):
                    if not session.create_new_account(logged_in):
                        continue
                else:
                    print("\n\tYou have decided to not create an account.")
                continue
            
            # If accounts detected, prints all accounts to the user.
            if accounts:
                print("\n\tAll your accounts:")
                n = 1
                for account in accounts:
                    sleep(0.1)
                    print("\n\n------------------------------------------")
                    print(f"\t\tAccount {n}:")
                    print("------------------------------------------")
                    print(f"\tAccount number:   {account["account_number"]}")
                    print(f"\tAccount balance:",end="")
                    print(f"  {account["balance"]:.2f} {account["currency"]}")
                    print(f"\tAccount user:     {account["person_number"]}")
                    n += 1
                print("------------------------------------------\n")

                # Allows user to select one of these accounts, 
                # via typing that accounts account_number
                print("\tPick one of your accounts to access.")
                user_accounts = []
                for account in accounts:
                    user_accounts.append(account["account_number"])
                selected_id = account_select(user_accounts)
                selected_account = session.db.db_selectAccount(selected_id)
                live_account = session.load_account(selected_account)
                
        # Create new account path
        elif account_path == "2":
            while True:
                session.create_new_account(logged_in)
                if pathYesNo("\n\tCreate another account?"):
                    continue
                else:
                    break
            continue  
        
        # Logout Path
        elif account_path == "3":
            if pathYesNo("\n\tConfirm logout?"):
                break
            else:
                continue

        # Account Selected Path Loop
        while True:
            print(f"\n\n\tAccount number {selected_id} selected\n")
            print("\tWhat do you want to do with this account?\n")
            print("\t1. Withdrawal")
            print("\t2. Deposit")
            print("\t3. Transfer")
            print(f"\t4. Change currency type: Current ['{live_account.currency}'.]")
            print(f"\t5. Back to account select\n")

            # Account action path.
            option = pathChooseXnumber(5,"Select option 1-5: " )

            # Account balance Withdrawal path
            if option == "1":


                withdraw = Withdraw(live_account)
                op_result = withdraw.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tWithdrawal Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:  {live_account.account_number}")
                    print(f"\tAccount balance: ",end="") 
                    print(f"{live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:    {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("Withdrawal failed. Choose another option.")
                    continue



            # Account balance Deposit path
            elif option == "2":
                
                deposit = Deposit(live_account)
                op_result = deposit.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tDeposit Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:  {live_account.account_number}")
                    print(f"\tAccount balance: ",end="") 
                    print(f"{live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:    {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("Deposit failed. Choose another option.")
                    continue
            

            # Account balance Transfer path
            elif option == "3":
                transfer_id = transfer_account_input()
                transfer_account = session.db.db_selectAccount(transfer_id)
                to_account = session.load_account(transfer_account)
                transfer = Transfer(live_account, to_account)

                op_result = transfer.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    session.db.db_save_Account(to_account)
                    print("\n\tTransfer Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:  {live_account.account_number}")
                    print(f"\tAccount balance: ",end="") 
                    print(f"{live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:    {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("\n\tTransfer failed. Choose another option.")
                    continue
                
            # Account currency Converter path
            elif option == "4":
                convert = ConvertCurrency(live_account)
                op_result = convert.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tConversion Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:  {live_account.account_number}")
                    print(f"\tAccount balance: ",end="") 
                    print(f"{live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:    {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("\n\tCurrency conversion failed. Choose another option.")
                    continue
            # Account select backtrack path
            elif option == "5":
                break
            
            
            

            
