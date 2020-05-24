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
    """
    LoginAndRegister class. 
    
    Mainly handles user authentication and register. 
    This class also handles the encryption and decryption of passwords.
    """
	
    def __init__(self):
        """
        Empty Constructor
        """
        pass
        
	
    def authenticate(self, username, password):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to authenticate user logging in
        
        Parameters:
                username(str): Username from user input
                password(str): Password from user input
		
        Returns:
                status(boolean): Indicator with true if verified or false if unverified 
        """
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
    
    def generate_key(self):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to generate a key for encryption
        
        Parameters:
                None
		
        Returns:
                Key: Key used for encryption and decryption
        """
        password = b"password"
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
    
    def encryptPassword(self, password):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to encrypt password
        
        Parameters:
                password(str): Plaintext password from user input
            
        Returns:
                encrypted(byte): Encrypted password
        """
        f = Fernet(self.generate_key())
        encrypted = f.encrypt(password.encode('utf-8'))
        return encrypted
        
    def decryptPassword(self, encrypted_password):
        """
        Task A
        
        Written by: Ching Loo(s3557584)
        
        Function to decrypt encrypted password
        
        Parameters:
                encrypted_password(byte): ciphertext password from database
            
        Returns:
                password(str): plaintext password
        """
        f = Fernet(self.generate_key())
        toDecrypt = encrypted_password.encode('utf-8')
        decrypted = f.decrypt(toDecrypt)
        password = decrypted.decode('utf-8')
        
        return password
        
    def enterUsername(self, username):
        """
        Task A
        
        Written by:Jason, Ching(s3557584), Lin
        
        Function to take user input and validate username for register
        
        Parameters:
                username(str): username from user input
            
        Returns:
                status(boolean): Indicator with true if verified or false if unverified 
        """
        status = False
        while status == False:
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
    
    
    #Written by:Jason, Ching, Lin
    """
    Function to take user input and validate for 1st name and surname for register
    """
    def enterName(self, firstName, surname):
        """
        Task A
        
        Written by:Jason, Ching(s3557584), Lin
        
        Function to take user input and validate first name and sur name for register
        
        Parameters:
                firstname(str): first name from user input
                surname(str): sur name from user input
            
        Returns:
                status(boolean): Indicator with true if verified or false if unverified 
        """
        status = False 
        
        #Regex pattern for validation for 1st name and surname
        regex = re.compile('[a-zA-Z]') 
        while status == False:
        
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
                
    def enterPassword(self, password, confirmPassword):
        """
        Task A
        
        Written by:Jason, Ching(s3557584), Lin
        
        Function to take user input and validate for password for register
        
        Parameters:
                password(str): password from user input
                confirmPassword(str): confirm password from user input
            
        Returns:
                status(boolean): Indicator with true if verified or false if unverified 
        """
        status = False
        while status == False:
            
            #Checking if the password entered has met the mentioned requirements
            #And simillar to the confirm password field
            if password == confirmPassword and re.match('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', password):
                status = True
                return status
            else:
                print("Either confirm password is not matched or password does not met the requirements")
                status = False
                return status
