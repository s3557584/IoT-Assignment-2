from DatabaseUtil import DatabaseUtil
from Validator import Validator

class Register:

    def __init__(self):
        self.__dao = DatabaseUtil()
        self.__new_username = None
        self.__new_fullname = None
        self.__new_password = None

    def ask_for_username(self):
        is_valid = False
        while not is_valid:
            username = input('Please input a user name here: \n' '(Only letters and numbers are allowed, 4 charactersmin)')
            username = username.strip()
            is_input_valid = Validator.validate_username(username)
            username_exists = self.__dao.check_if_username_exists(username)
            is_valid = is_input_valid and not username_exists
            if not is_input_valid:
                print('Username entered does not meet the requirement')
            if username_exists:
                print('The username is already taken, please user another name')

        self.__new_username = username
    
    def ask_for_fullname(self):
        is_valid = False
        while not is_valid:
            fullname = input("Please enter your full name in <First Name> <Last Name> format")
            fullname = fullname.strip()
            is_valid = Validator.validate_fullname(fullname)
            if not is_valid:
                print("Full name entered does not meet the requirement")
        self.__new_fullname = fullname

    def ask_for_password(self):
        is_valid = False
        while not is_valid:
            password = input("Enter password")
            password = password.strip()
            is_valid = Validator.validate_password()
            if not is_valid:
                print("Password entered does not meet the requirement")
                #verify password here
        self.__new_password = password


    def register_user(self):
        if self.__new_username is None:
            print("Error: username not found")
            return
        if self.__new_fullname is None:
            print("Error: fullname not found")
            return
        if self.__new_password is None:
            print("Error: password not found")
            return
        self.__dao.insert_user(username = self.__new_username, fullname = self.__new_fullname, password = self.__new_password)
        print("Registration completed")