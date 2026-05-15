import requests

VALIDATION_CONFIGURATIONS = {
'name': {'charmax': 15, 'charmin': 1, 'digitonly': False, 'lettersonly': True, 'message': "\nFull name: "},

'person_number': {'charmax': 12, 'charmin': 12, 'digitonly': True, 'lettersonly': False, 'message': "Complete personnummer(full years): "  },

'email': {'charmax': 80, 'charmin': 6, 'digitonly': False, 'lettersonly': False, 'message': "Email address: "  },

'phonenumber': {'charmax': 15, 'charmin': 7, 'digitonly': True, 'lettersonly': False, 'message': "Phone number: "  },

'street': {'charmax': 80, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Street address: "  },

'post_number': {'charmax': 10, 'charmin': 4, 'digitonly': True, 'lettersonly': False, 'message': "Postnumber: "  },

'city': {'charmax': 85, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "City: "  },

'country': {'charmax': 56, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Country: "  }
}
VALIDATE_PASSWORD = {'password': {'charmax': 40, 'charmin': 10, 'digitonly': False, 'lettersonly': False, 'message': "Password: " }}

ALLOWED_CURRENCIES = ["SEK","USD","GBP","EUR","CNY"]

# CHOICES:

def multiValidationInput(keyname, keyconfig):
    while True:   
        try:    
            userinput = input(f"\t{keyconfig['message']}")
            if len(userinput) < keyconfig['charmin']:
                raise ValueError(f'\tInput {keyname} is too short! Minimum {keyconfig["charmax"]} characters!')
               
            if len(userinput) > keyconfig['charmax']:
                raise ValueError(f'\tInput {keyname} is too long! Maximum {keyconfig["charmax"]} characters!')
                
            if keyconfig['lettersonly'] and not userinput.replace(" ","").isalpha():
                raise ValueError(f'\t{keyname} must only contain letters! No numbers/other characters.')

            if keyconfig['digitonly'] and not userinput.replace(" ","").isdigit():
                raise ValueError(f'\t{keyname} must only contain numbers! No letters/other characters.')

        except(KeyError,ValueError,TypeError):
            print(f"\n\tSomething went wrong during {keyname} input.\n")
            if pathYesNo("Try again?"):
                continue
            else:
                return False  
        return userinput
    
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

def create_person_input():
    adressitems = ["street","post_number","city","country"]
    new_profile = {}
    new_profile["adress"] = {}
    for keyname , keyconfig in VALIDATION_CONFIGURATIONS.items():
        if keyname in adressitems:
            temp = multiValidationInput(keyname,keyconfig)
            new_profile["adress"][keyname] = temp
        else:
            temp = multiValidationInput(keyname,keyconfig)
            new_profile[keyname] = temp
    return new_profile
# def account_currency_select():
#     while True:
#         print("""\tSelect a currency type for your account.
#             This will be the currency type for your entire balance tied to this account.
#             This can be changed at a later date!""")
#         currency = currency_select()
#         if currency == "":
#             print("\t\nEmpty input detected, please pick a currency type!\n\n")
#             continue
#         elif currency in ALLOWED_CURRENCIES:
#             return currency
#         else:
#             print("We do not support this currency type.")
#             print("Pick a new currency or cancel account creation?")
#             print("Type 'new' to select a new currency. " \
#             "Otherwise press enter to cancel creation.")
#             choose = input("new or cancel: ")
#             choose = choose.strip().lower()
#             while True:
#                 choose = pathChooseXnumber(2,"Select option 1-2:")
#                 if choose == "1":
#                     break
#                 elif choose == "2":
#                     return False
#             continue

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
                print("\tTry again?")
                choice = input("y/n")
                if choice.lower() == "y":
                    continue
                else:
                    break

        except ValueError:
            print("\tWe only accept numbers, be careful when typing,",end="")
            print("dont add spaces/letters")

def transfer_account_input():
    print("\n\n\tYou have chosen to transfer balance to another account!")
    while True:
        try:
            account = input("\n\tEnter reciever account number: ")
            account = int(account)
            return account
        except ValueError:
            print("\tWe only accept numbers, be careful when typing,",end="")
            print("dont add spaces/letters")


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