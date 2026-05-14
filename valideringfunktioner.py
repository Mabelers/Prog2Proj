import requests

VALIDATION_CONFIGURATIONS = {
'name': {'charmax': 15, 'charmin': 1, 'digitonly': False, 'lettersonly': True, 'message': "Complete name: "},

'person_number': {'charmax': 11, 'charmin': 11, 'digitonly': True, 'lettersonly': False, 'message': "Complete personnummer: "  },

'email': {'charmax': 80, 'charmin': 6, 'digitonly': False, 'lettersonly': False, 'message': "Email address: "  },

'phonenumber': {'charmax': 15, 'charmin': 7, 'digitonly': True, 'lettersonly': False, 'message': "Phone number: "  },

'street': {'charmax': 80, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Street address: "  },

'post_number': {'charmax': 10, 'charmin': 4, 'digitonly': True, 'lettersonly': False, 'message': "Postnumber: "  },

'city': {'charmax': 85, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "City: "  },

'country': {'charmax': 56, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Country: "  }
}
ALLOWED_CURRENCIES = ["SEK","USD","GBP","EUR","CNY"]

def multiValidationInput(keyname, keyconfig):
    while True:   
        try:    
            userinput = input(keyconfig["message"])
            if len(userinput) < keyconfig['charmin']:
                raise ValueError(f'\t\Input {keyname} is too short! Minimum {keyconfig['charmax']} characters!')
               
            if len(userinput) > keyconfig['charmax']:
                raise ValueError(f'\t\Input {keyname} is too long! Maximum {keyconfig['charmax']} characters!')
                
            if keyconfig['lettersonly'] and not userinput.replace(" ","").isalpha():
                raise ValueError(f'{keyname} must only contain letters! No numbers/other characters.')

            if keyconfig['digitonly'] and not userinput.replace(" ","").isdigit():
                raise ValueError(f'{keyname} must only contain numbers! No letters/other characters.')

        except(KeyError,ValueError,TypeError):
            print(f"Something went wrong during {keyname} input. Try again?")
            x = input("Y/N")
            if x.lower() == "y":
                continue
            else:
                print("Fatal error in input, program exit.")
                exit()
        except:
                print("Fatal error in input, program exit.")
                exit()
        return userinput
    
def CreateValidPass():

    while True:
        password = input("Enter new password: ")
        if len(password) < 10:
            print("Password too short! Min 10 characters. Try again!")
            continue
        if len(password) > 40:
            print("Password too long! Max 40 characters. Try again!")
            continue
        for char in password:
            if char.isdigit():
                break
        else:
            print("At least one number required!")
            continue
        for char in password:
            if char.isupper():
                break
        else:
            print("At least one capital letter required!")
            continue
        
        validatepw = input("Confirm password: ")
        if password != validatepw:
            print("Passwords don't match!")
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
def account_currency_select():
    while True:
        print("""Select a currency type for your account, 
            this will be the currency type for your entire balance tied to this account 
            \nThis can be changed at a later date!""")
        print("Supported currency types are: ")
        for curr in ALLOWED_CURRENCIES:
            print(f"\t{curr}\n")
        currency = input("Your Choice: ")
        currency = currency.strip().upper()
        if currency == "":
            print("Empty input detected, please pick a currency type!\n\n")
            continue
        elif currency in ALLOWED_CURRENCIES:
            return currency
        else:
            print("We do not support this currency type.")
            print("Pick a new currency or cancel account creation?")
            print("Type 'new' to select a new currency. " \
            "Otherwise press enter to cancel creation.")
            choose = input("new or cancel: ")
            choose = choose.strip().lower()
            if choose == "new":
                continue
            else:
                return False

def currency_select():
    print("Please pick a currency:\n")
    for curr in ALLOWED_CURRENCIES:
        print(f"\t{curr}")
    currency = input("Your Choice: ")
    while currency not in ALLOWED_CURRENCIES:
        print("Invalid currency type")
        currency = input("Your Choice: ")
    return currency

def balance_input(type):
    while True:
        try:
            amount = input(f"{type} amount: ")
            amount = float(amount)

            if amount >= 999999:
                print(f"""{amount:.2f} is too high. Maximum {type}
                       amount is 999 999 no matter currency types.""")
                continue
            elif amount == 0:
                print(f"You cannot {type} 0 balance.")
                continue
            elif amount < 0: 
                print(f"Only positive numbers allowed on {type}")
                continue
            else:
                return amount
                    
        except ValueError:
            print("""Only numbers, be careful when typing,
                    \ndont add spaces/letters""")
        except:
            print("Unknown issue, try again.")

def account_select(accounts):
    while True:
        try:
            account = input("Account: ")
            account = int(account)
            if account in accounts:
                print(f"Account: {account} confirmed.")
                return account
            else: 
                print("Incorrect account number.")
                print("Try again?")
                choice = input("y/n")
                if choice.lower() == "y":
                    continue
                else:
                    break

        except ValueError:
            print("""We only accept numbers, be careful when typing,
                  \ndont add spaces/letters""")
        except:
            print("Unknown issue, try again.")
def transfer_account_input():
    print("You have chosen to transfer account")
    while True:
        try:
            account = input("Enter account number: \n")
            account = int(account)
            return account
        except ValueError:
            print("""We only accept numbers, be careful when typing,
                  \ndont add spaces/letters""")
        except:
            print("Unknown issue, try again.")

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
    except requests.exceptions.HTTPError:
        print("API HTTP error")
    except requests.exceptions.JSONDecodeError:
        print("JSON decode error")
    except (ValueError,KeyError):
        print("API format mismatch")
    return False