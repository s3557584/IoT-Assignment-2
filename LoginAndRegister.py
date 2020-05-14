from DatabaseUtil import DatabaseUtil
import re
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
utilsObj = DatabaseUtil()
class LoginAndRegister:
	
	# Constructor
    def __init__(self):
        pass
        
	# Function to authenticate user logging in
    def authenticate(self, username, password):
        status = False 
        encrypted_password = ""
        
        with utilsObj.connection.cursor() as cursor:
            
            # Executing SQL query to authenticate user
            if cursor.execute("SELECT * FROM user WHERE username = (%s)", [(username)]):
            
                results = cursor.fetchall()
            
            # If Username matches fetch encrypted password
                for i in results:
                    encrypted_password = i[4]
                
                decryptedPassword = self.decryptPassword(encrypted_password)
            # Calls function to verify encrypted password. 
            # If match returns true so that user is logged in.
                if decryptedPassword == password:
                    status = True
            else:
                status = False
                
            cursor.close()
            return status
    
    #Function to generate a key for encryption
    def generate_key(self):
        password_provided = "password"
        password = password_provided.encode()
        salt = b'Oy\nK5o\x15\xa8ex2U\x94A\xb9\x8c'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    # Function to encrypt password
    def encryptPassword(self, password):
        message = password.encode()
        f = Fernet(self.generate_key())
        encrypted = f.encrypt(message)
        return encrypted
        
    # Function to decrypt encrypted password
    def decryptPassword(self, encrypted_password):
        f = Fernet(self.generate_key())
        decrypted = f.decrypt(encrypted_password)
        return decrypted
        
    # Function to take user input and validate username for register
    def enterUsername(self, username):
        status = False
        while status == False:
            #username = raw_input("Please enter a username: ")
            with utilsObj.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM user WHERE username = (%s)", [(username)])
                #To check if username already exist or not
                if cursor.fetchall():
                    print("Username already exists please enter another one")
                    status = False
                    return status
                #To check if username if left empty or not
                elif username == "":
                    print("Username can't be empty")
                    status = False
                    return status
                else:
                    status = True
                    return status
    
    #Function to take user input and validate for 1st name and surname for register
    def enterName(self, firstName, surname):
        status = False 
        #Regex pattern for validation for 1st name and surname
        regex = re.compile('[a-zA-Z]') 
        while status == False:
            #firstName = raw_input("Enter your first name: ")
            #surname = raw_input("Enter your surname: ")
            #Check if both of the fields are empty or not
            if firstName == "" or surname == "":
                print("Please enter your first name and surname")
                status = False
                return status
            #Check if both of the fields contain only letters or not
            elif regex.search(firstName) == None or regex.search(surname) == None:
                print("First name and surname can't contain any special characters or numbers")
                status = False
                return status
            else:    
                status = True
                return status
                
    #Function to take user input and validate for password for register
    def enterPassword(self, password, confirmPassword):
        status = False
        while status == False:
            #password = raw_input("Enter your password\n(Min 6 and Max 20)\n(Must have one number, lowercase, uppercase and special character)\n: ")
            #confirmPassword = raw_input("Confirm password: ")
            #Checking if the password entered has met the mentioned requirements
            #And simillar to the confirm password field
            if password == confirmPassword and re.match('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', password):
                status = True
                return status
            else:
                print("Either confirm password is not matched or password does not met the requirements")
                status = False
                return status
