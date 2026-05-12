
VALIDATION_CONFIGURATIONS = {
'name': {'charmax': 15, 'charmin': 1, 'digitonly': False, 'lettersonly': True, 'message': "Complete name: "},

'person_number': {'charmax': 11, 'charmin': 11, 'digitonly': True, 'lettersonly': False, 'message': "Complete personnummer: "  },

'email': {'charmax': 80, 'charmin': 6, 'digitonly': False, 'lettersonly': False, 'message': "Email address: "  },

'phonenumber': {'charmax': 15, 'charmin': 7, 'digitonly': True, 'lettersonly': False, 'message': "Phone number: "  },

'street': {'charmax': 80, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Street address: "  },

'post_number': {'charmax': 10, 'charmin': 4, 'digitonly': True, 'lettersonly': False, 'message': "Postnumber: "  },

'city': {'charmax': 85, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "City: "  },

'country': {'charmax': 56, 'charmin': 2, 'digitonly': False, 'lettersonly': False, 'message': "Country: "  },

'password': {'charmax': 50, 'charmin': 10, 'digitonly': False, 'lettersonly': False, 'message': "Password for new user: "  }
}


def multiValidationInput(keyname, keyconfig):
    while True:   
        try:    
            userinput = input(keyconfig["message"])
            if len(userinput) < keyconfig['charmin']:
                print(f'\t\Input {keyname} is too short! Minimum {keyconfig['charmax']} characters!')
                
            if len(userinput) > keyconfig['charmax']:
                print(f'\t\Input {keyname} is too long! Maximum {keyconfig['charmax']} characters!')
                
            if keyconfig['lettersonly'] and not userinput.replace(" ","").isalpha():
                raise ValueError(f'{keyname} must only contain letters! No numbers/other characters.')

            if keyconfig['digitonly'] and not userinput.replace(" ","").isdigit():
                raise ValueError(f'{keyname} must only contain numbers! No letters/other characters.')

        except(KeyError,ValueError,TypeError):
            print(f" went wrong during {keyname} input. Try again?")
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
    
def passwordValidation(password):
    


	    #     if key['lettersonly'] and not output.replace(" ", "").isalpha():
        #             raise ValueError(f'{key} must only contain letters! No numbers/other characters.')
        # except:
        #     continue
		# 	#     if letters_only == False:
		# 	# 		print(f'\t\tDitt namn får endast innehålla bokstäver!')
		# 	# 		continue
			# 	if letters_only == True:
			# 		pass
			# if text.isdigit() is True:
			# 	print(f'\t\tDitt {prompt2} får inte bestå av endast siffror! '
			# 		'Minst en bokstav!')
			# 	continue
			# for char in text:
			# 	if char in ':;!"#¤%&/()=?@£$€{[]}':
			# 		print(f'\t\tDitt {prompt2} får endast innehålla bokstäver och'
			# 			 ' siffror! Specialtecken som ":;!"#¤%&/()=?@£$€{[]}" är '
			# 			 'inte tillåtna!\n\t\tFörsök igen!')
					# break
		# 	else:$
		# 		return text
		# except ValueError:
		# 	print(prompt3)
		# 	continue
		# except KeyboardInterrupt:
		# 	print('\n\t\tProgrammet avbröts av användaren pga avbryt "CTRL+C"')
		# 	exit()
		# except:
		# 	print('\n\t\tProgrammet har påstått ett oväntat fel. Försök igen')
		# 	exit()
