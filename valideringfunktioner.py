import requests

# Input validation configuration. 
# Decides on allowed states of different input types during input.
# Allows for error handling and data integrity.
VALIDATION_CONFIGURATIONS = {
'name': 
{
'charmax': 30,
'charmin': 1, 
'digitonly': False, 
'lettersonly': True, 
'message': "\n\tFull name: "
},

'person_number': 
{
'charmax': 12, 
'charmin': 12, 
'digitonly': True, 
'lettersonly': False, 
'message': "Complete personnummer(full years): "
},

'email': 
{
'charmax': 80, 
'charmin': 6, 
'digitonly': False, 
'lettersonly': False, 
'message': "Email address: "  
},

'phonenumber': 
{
'charmax': 15, 
'charmin': 7, 
'digitonly': True, 
'lettersonly': False, 
'message': "Phone number: "  
},

'street': 
{
'charmax': 80, 
'charmin': 2, 
'digitonly': False, 
'lettersonly': False, 
'message': "Street address: "
},

'post_number': 
{
'charmax': 10, 
'charmin': 4, 
'digitonly': True, 
'lettersonly': False, 
'message': "Postnumber: "
},

'city': 
{
'charmax': 85, 
'charmin': 2, 
'digitonly': False, 
'lettersonly': False, 
'message': "City: "  
},

'country': 
{
'charmax': 56, 
'charmin': 2, 
'digitonly': False, 
'lettersonly': False, 
'message': "Country: "  
}
}

# Password input configuration, allows to validate password.
# Seperate from other inputs, since password is applied after,
# and the others are validated in an iteration.
VALIDATE_PASSWORD = {
'password': 
{
'charmax': 40, 
'charmin': 10, 
'digitonly': False, 
'lettersonly': False, 
'message': "Password: " 
}}

# Small list of allowed currencies.
# To add more, make sure the short term is correct.
# APIs will automatically accept this new currency in this list.
# And user creation will allow switching to it.
# As long as the 3 letter word is correct.
ALLOWED_CURRENCIES = ["SEK","USD","GBP","EUR","CNY"]


# Validation funciton for most inputs.
# param1: keyname, the name of current value being set. Used for prints.
# param2: keyconfig, the configuration for said value type.
# Function takes input value, does error handling,
# and makes sure the input is within configuration specifications
def multiValidationInput(keyname, keyconfig):
    while True:   
        try:    
            userinput = input(f"\t{keyconfig['message']}")
            replaced = userinput.replace(" ","")
            if len(userinput) < keyconfig['charmin']:
                raise ValueError(f'''\tInput {keyname} is too short!
        Minimum {keyconfig["charmin"]} characters!''')
               
            if len(userinput) > keyconfig['charmax']:
                raise ValueError(f'''\tInput {keyname} is too long! 
        Maximum {keyconfig["charmax"]} characters!''')
                
            if keyconfig['lettersonly'] and not replaced.isalpha():
                raise ValueError(f'''\t{keyname} must only contain letters!
        No numbers/other characters.''')

            if keyconfig['digitonly'] and not replaced.isdigit():
                raise ValueError(f'''\t{keyname} must only contain numbers!
        No letters/other characters.''')

        except ValueError as e:
            print(e)
            if pathYesNo("Try again?"):
                continue
            else:
                return False  
        except(KeyError, TypeError):
            print(f"\n\tConfig error during {keyname} input.\n")
            exit()
        return userinput

# Password creation function:
# Called during password creation, uses password validation 
# according to a preset configuration
def CreateValidPass():

    while True:
        password = input("\t\nEnter new password: ")
        if len(password) < 10:
            print("\t\nPassword too short! Min 10 characters. Try again!")
            continue
        if len(password) > 40:
            print("\t\nPassword too long! Max 40 characters. Try again!")
            continue
        for char in password:
            if char.isdigit():
                break
        else:
            print("\t\nAt least one number required!")
            continue
        for char in password:
            if char.isupper():
                break
        else:
            print("\t\nAt least one capital letter required!")
            continue
        
        validatepw = input("\t\nConfirm password: ")
        if password != validatepw:
            print("\t\nPasswords don't match!")
            continue
        else:
            return password

# User creation function:
# Creates the user dictionary, with a nested adress key as its own dict
# Through iterations and conditions, 
# all keynames in list adressitems, is filtered into its own dict
# This way the User is created, with the nested adress informaton.
def create_person_input():
    adressitems = ["street","post_number","city","country"]
    new_profile = {}
    new_profile["adress"] = {}
    for keyname , keyconfig in VALIDATION_CONFIGURATIONS.items():     
            if keyname in adressitems:        
                temp = multiValidationInput(keyname,keyconfig)
                if temp == False:
                    return False
                else:  
                    new_profile["adress"][keyname] = temp
            else:
                
                temp = multiValidationInput(keyname,keyconfig)
                if temp == False:
                    return False
                new_profile[keyname] = temp
            
    return new_profile


# Currency select function:
# Iterates through all ALLOWED_CURRENCIES, which acts as a whitelist for user
# input. Only value that passes whitelist validation may be returned.
# Also prints all supported types for user visual.
def currency_select():
    print("\n\tSupported currency types:\n")
    print("\t",end="")
    for curr in ALLOWED_CURRENCIES:
        print(f"{curr}  ",end="")
    currency = input("\n\n\tYour Choice: ")
    while currency not in ALLOWED_CURRENCIES:
        print("\n\tInvalid currency type\n")
        print("\n\tSupported currency types:\n\t")
        for curr in ALLOWED_CURRENCIES:
            print(f"{curr}  ",end="")
        currency = input("\n\tYour Choice: ")
    return currency

# Number validation function:
# Validation of a user balance input.
# Used for deposit, withdrawal and transfer of balance.

def balance_input(type):
    while True:
        try:
            amount = input(f"\n\t{type} amount: ")
            amount = float(amount)

            if amount >= 999999:
                print(f"""\n\t{amount:.2f} is too high. Maximum {type}
                       amount is 999 999 no matter currency types.""")
                continue
            elif amount == 0:
                print(f"\n\tYou cannot {type} 0 balance.")
                continue
            elif amount < 0: 
                print(f"\n\tOnly positive numbers allowed on {type}")
                continue
            else:
                return amount
                    
        except ValueError:
            print("\tWe only accept numbers, be careful when typing,",end="")
            print("dont add spaces/letters")
            continue


# Account select function:
# param: List of all account numbers available to this user account.
# Allows for fast user input, list is used as a whitelist, 
# only items listed inside the param, will return the
# correct account type user specified
def account_select(accounts):
    while True:
        try:
            print(f"\t{accounts}")
            account = input("\tAccount: ")
            account = int(account)

            if account in accounts:
                print(f"\tAccount: {account} confirmed.")
                return account
            else: 
                print("\tIncorrect account number.")
            if pathYesNo("Try again?"):
                continue
            else:
                return False 

        except ValueError:
            print("\tWe only accept numbers, be careful when typing,",end="")
            print("dont add spaces/letters")

# Direct integer input, with validation.
# Used for selecting a bank account number, to transfer funds to.
def transfer_account_input():
    print("\n\n\tYou have chosen to transfer balance to another account!")
    while True:
        try:
            account = input("\n\tEnter reciever account number: ")
            account = int(account)
            return account
        except ValueError:
            print("\tWe only accept whole numbers,",end="")
            print(" be careful when typing, dont add spaces/letters")


# Function fetches current exchange rate between 2 currencies.
# param: from_currency: Current currency type. 
# param: to_currency: To currency type. 
# return: value: Current exchange rate in decimal float param1 and param2
def currency_fetch(from_currency, to_currency):

    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        urlresponse = requests.get(url)
        urlresponse.raise_for_status()
        parsed = urlresponse.json()
        return parsed["rates"][to_currency]
    
    except requests.exceptions.ConnectionError:
        print("API connection unavailable")
    except requests.exceptions.Timeout:
        print("API request timeout")
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Status code: {urlresponse.status_code}")
        print(f"Response: {urlresponse.text}")

    except requests.exceptions.JSONDecodeError:
        print("JSON decode error")
    except (ValueError,KeyError):
        print("API format mismatch")
    return False
def pathYesNo(message):
    while True:
        path = input(f"\t{message} (y/n): ").strip().lower()
        if path == "y":
            return True
        elif path == "n":
            return False
        else:
            print("\tInvalid input, only input y or n.")


def pathChooseXnumber(ranges,prompt):
    while True:
        x = []
        for n in range(1,ranges + 1):
            n = str(n)
            x.append(n)
        a = input(f"\t{prompt}")
        if a in x:
            return a
        else:
            print(f"\tPick a number between 1-{ranges}\n")