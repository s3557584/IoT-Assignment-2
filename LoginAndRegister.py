from DatabaseUtil import DatabaseUtil
import hashlib, binascii, os
utilsObj = DatabaseUtil()
class LoginAndRegister:
	
	# Constructor
    def __init__(self):
        pass
        
	# Function to authenticate user logging in
    def authenticate(self):
        status = False 
        encrypted_password = ""
        username = raw_input("Enter you username: ")
        password = raw_input("Please enter your password:")
        
        with utilsObj.connection.cursor() as cursor:
            
            # Executing SQL query to authenticate user
            cursor.execute("SELECT * FROM users WHERE username = (%s)", [(username)])
            
            results = cursor.fetchall()
            
            # If Username matches fetch encrypted password
            for i in results:
                encrypted_password = i[4]
            
            # Calls function to verify encrypted password. 
            # If match returns true so that user is logged in.
            if self.verify_password(encrypted_password, password):
                status = True
                for i in results:
                    print("Welcome " + i[2])
                    
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
