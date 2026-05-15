from banklogic import Service
from time import sleep
from classes import *
from database import Customers
from valideringfunktioner import *  

# REMINDER ADD COMMIT AND DISCONNECT BEFORE TESTING.

# Main loop for whole program, allows for seamless
# logout to login to new user.
while True:
    
    # Loop for login/registration
    while True:
        print("\n\tWelcome to Marcus banking system")
        print("\tChoose one of following options: \n")
        print("\t1. Login to bank")
        print("\t2. Register with us")
        print("\t3. Exit system\n")


        # Decide program path
        choose = pathChooseXnumber(3,"Select option 1-3: " )

        # Start initial object, connects to database.
        db = Customers()
        session = Service(db)

        # Login option, requires previous registration
        if choose == "1":
            print("")
            logged_in = session.login()
            if not logged_in:
                continue
            break
            
        # Registration option. Adds user to DB.
        elif choose == "2":
            print("\n\tYou have chosen to register at our bank.")
            print("\tYou will now be guided through the registration process.")

            # Creates new user,
            result = session.create_new_user()
            if result == False:
                print("\n\tAn error has occured in the program.")
                print("\tCurrently we dont support these bugs, ",end="")
                print("program will now shutdown.")
                exit()
                
            elif result == "login":
                logged_in = session.login()
                
                if not logged_in:
                    continue
                break
                
            elif result == True:
                print("\tRegistration complete.")
        
        # Exits program, 
        elif choose == "3":
            print("Exiting bank system, have a good day!")
            exit()

    # Loop for account selection / account creation.
    while True:
        #select
        print("\n\tWhat are we doing today?\n")
        print("\t1. Select an existing account")
        print("\t2. Create new account")
        print("\t3. Logout from bank\n")
        account_path = pathChooseXnumber(3,"Select option 1-3: ")

        # Account select path, checks if there are accounts to be selected.
        # if not, acts like a 2nd create account.
        if account_path == "1":
            accounts = session.db.db_fetchAccounts(logged_in.person_number)
            if not accounts:
                print("\n\tIt appears you do not have an account registered with us yet.")
                print("\n\tDo you want to create an account? To use our bank you have to.")
                if pathYesNo("Create account?"):
                    if not session.create_new_account(logged_in):
                        continue
                else:
                    print("\n\tYou have decided to not create an account.")
                continue
            if accounts:
                print("\n\tAll your accounts:")
                n = 1
                for account in accounts:
                    sleep(0.1)
                    print("\n\n------------------------------------------")
                    print(f"\t\tAccount {n}:")
                    print("------------------------------------------")
                    print(f"\tAccount number:    {account["account_number"]}")
                    print(f"\tAccount balance:   {account["balance"]:.2f} {account["currency"]}")
                    print(f"\tAccount user:      {account["person_number"]}")
                    n += 1
                print("------------------------------------------\n")
                print("\tPick one of your accounts to access.")
                user_accounts = []
                for account in accounts:
                    user_accounts.append(account["account_number"])
                selected_id = account_select(user_accounts)
                selected_account = session.db.db_selectAccount(selected_id)
                live_account = session.load_account(selected_account)
                

        elif account_path == "2":
            while True:
                session.create_new_account(logged_in)
                if pathYesNo("\n\tCreate another account?"):
                    continue
                else:
                    break
            continue  
                
        elif account_path == "3":
            if pathYesNo("\n\tConfirm logout?"):
                break
            else:
                continue

        #selected
        while True:
            print(f"\n\n\tAccount number {selected_id} selected\n")
            print("\tWhat do you want to do with this account?\n")
            print("\t1. Withdrawal")
            print("\t2. Deposit")
            print("\t3. Transfer")
            print(f"\t4. Change currency type: Current ['{live_account.currency}'.]")
            print(f"\t5. Back to account select\n")

            # Path decider function.
            option = pathChooseXnumber(5,"Select option 1-5: " )

            # Account balance Withdrawal
            if option == "1":


                withdraw = Withdraw(live_account)
                op_result = withdraw.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tWithdrawal Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:    {live_account.account_number}")
                    print(f"\tAccount balance:   {live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:      {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("Withdrawal failed. Choose another option.")
                    continue



            # Account balance Deposit
            elif option == "2":
                
                deposit = Deposit(live_account)
                op_result = deposit.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tDeposit Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:    {live_account.account_number}")
                    print(f"\tAccount balance:   {live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:      {live_account.person_number}")
                    print("------------------------------------------\n")
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
                    print("\n\tTransfer Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:    {live_account.account_number}")
                    print(f"\tAccount balance:   {live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:      {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("\n\tTransfer failed. Choose another option.")
                    continue
                
            # Account currency Converter
            elif option == "4":
                convert = ConvertCurrency(live_account)
                op_result = convert.transaction_type()
                if op_result:
                    session.db.db_save_Account(live_account)
                    print("\n\tConversion Successfull!")
                    print("\n\tUpdated account details: ")
                    print("------------------------------------------")
                    print(f"\tAccount number:    {live_account.account_number}")
                    print(f"\tAccount balance:   {live_account.balance:.2f} {live_account.currency}")
                    print(f"\tAccount user:      {live_account.person_number}")
                    print("------------------------------------------\n")
                else:
                    print("\n\tCurrency conversion failed. Choose another option.")
                    continue
                
            elif option == "5":
                break
            
            
            

            
