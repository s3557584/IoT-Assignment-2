import MySQLdb
import hashlib, binascii, os

class DatabaseUtil:
    HOST = "35.189.29.67"
    USER = "root"
    PASSWORD = "password"
    DATABASE = "IoTAssignment2"
    
    # Constructor
    def __init__(self, connection = None):
        
        #Checks if a connection has been made with DB
        if(connection == None):
            
            #If no establish a connection
            connection = MySQLdb.connect(DatabaseUtil.HOST, DatabaseUtil.USER,
                DatabaseUtil.PASSWORD, DatabaseUtil.DATABASE)
        self.connection = connection
        
    # Function to close the database connection
    def close(self):
        self.connection.close()
            
            
            
