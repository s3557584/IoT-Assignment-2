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
        
   
    def getVehicle(self, username):
        userID = 0
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT userID FROM users WHERE username = (%s)", [(username)])
            results = cursor.fetchall()
            for i in results:
                userID = i[0]
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleBrand, vehicleModel FROM vehicles WHERE userID = (%s)", [(userID)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
            
    def searchVehicle(self, userInput):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles WHERE vehicleBrand LIKE %s OR vehicleModel LIKE %s", [(userInput), (userInput)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
            
            
            
