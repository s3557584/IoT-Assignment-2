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
        
    #Function to display all vehicles the user is renting
    def getVehicle(self, username):
        userID = 0
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT userID FROM user WHERE username = (%s)", [(username)])
            results = cursor.fetchall()
            for i in results:
                userID = i[0]
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleBrand, vehicleModel FROM vehicle WHERE userID = (%s)", [(userID)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
    
    #Search vehicle function
    def searchVehicle(self, userInput):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicle WHERE vehicleBrand LIKE %s OR vehicleModel LIKE %s", [(userInput), (userInput)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
            
    def searchVehicleID(self,userInput):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleID FROM vehicle WHERE vehicleID = %s", [(userInput)])
            vehicleIDResult = cursor.fetchall()
            return vehicleIDResult
     
    def searchUserID(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT userID FROM user WHERE username = %s", [(username)])
            result = cursor.fetchall()
            return result
            
    def getVehicleStatus(self, vehicle_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT rentalStatus FROM vehicle WHERE vehicleID = %s",[(vehicle_id)])
            res = cursor.fetchall()
            #convert tuple to int
            result = int(res[0][0])
            return result
    
    def getUserID(self, vehicle_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT UserID FROM vehicle WHERE vehicleID = %s", [(vehicle_id)])
            result = cursor.fetchall()
            return result
            
    def getGCEID(self, vehicle_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT google_calendar_id FROM appointments WHERE vehicle_id = %s", [(vehicle_id)])
            result = cursor.fetchall()
            return result
            
    def deleteBooking(self, GCEID):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE google_calendar_id = %s", [(GCEID)])
            self.connection.commit()
            return
    
    def cancelVehicle(self, vehicle_id):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE vehicle SET rentalStatus = 1, userID = NULL WHERE vehicleID = (%s)", [(vehicle_id)])
            self.connection.commit()
            return
            
            
    #Update vehicle table function
    def updateVehicle(self, userInput):
        message = " "
        with self.connection.cursor() as cursor:
            rows_count = cursor.execute("SELECT rentalStatus, userID FROM vehicle WHERE vehicleID = (%s)", [(userInput)])
            vehicleResult = cursor.fetchall()
            #Checks if there is any results from the database
            if rows_count == 0:
                #If no result shows error message
                message = "Incorrect vehicle ID"
            else:
                status = " "
                userID = " "
                for i in vehicleResult:
                    status = i[0]
                    userID = i[1]
                #Checks if vehicle is already returned
                if status == 1 and userID is None:
                    #If yes show error message
                    message = "Vehicle is already returned!!"
                else:
                    #If validation has no errors update vehicle status accordingly
                    cursor.execute("UPDATE vehicle SET rentalStatus = 1, userID = NULL WHERE vehicleID = (%s)", [(userInput)])
                    self.connection.commit()
                    message = "Vehicle Returned!!"
            return message
            
    def book(self,user_id, vehicle_id):
        #update vehicle table
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE vehicle SET rentalStatus = 0, userID = (%s) WHERE vehicleID = (%s)", [(user_id), (vehicle_id)])
            self.connection.commit()
            print("Vehicle Booked!")
        return
        
            
            
                    
            
        
            
            
