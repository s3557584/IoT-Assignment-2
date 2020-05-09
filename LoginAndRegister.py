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
            if self.verify_password(encrypted_password, password):
                status = True
                utilsObj.close()
            return status
            
    # Function to verify encrypted password
    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password 
    
    def newUser(self):
        found = 0
        while found == 0:
            username = input ("Please enter a username: ")
            with utilsObj.connection.cursor() as db:
                cursor = db.cursor()
            findUser = ("SELECT * FROM user WHERE username = ?")
            cursor.execute(findUser, [(username)])

            if cursor.fatchall():
                print("Username Taken, please try again")
            else:
                found = 1
        
        firstnmae = input("Enter your first nmae:")
        surnmane = input("Enter your surname: ")
        password = input("please enter your password: ")
        password1 = input("please reneter your pssword")
        while password != password1:
            print("Your passwords didn't match, please try again ")
            password = input("please enter your password: ")
            password1 = input("please reneter your pssword")
        
        insertData = ''' INSERT INTO users(username,firstnme,surname,password)VALUES(?,?,?,?)'''
        cursor.execute(insertData,[(username),(firstnmae),(surnmane),(password)])
        db.commit()



        
