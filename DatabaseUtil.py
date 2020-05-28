import MySQLdb
import hashlib, binascii, os

class DatabaseUtil:
    """
    Task A and B
    
    DatabaseUtil class.
    
    This class mainly handles connection to the database.
    This class also handles fetching and editing data from the database
    """
    HOST = "35.189.29.67"
    USER = "root"
    PASSWORD = "password"
    DATABASE = "IoTAssignment2"
    
    
    def __init__(self, connection = None):
        """
        Constructor
        
        Establishes database connection
        
        Parameters:
			connection: Default is none
		
		Returns:
			None
        """
        
        #Checks if a connection has been made with DB
        if(connection == None):
            
            #If no establish a connection
            connection = MySQLdb.connect(DatabaseUtil.HOST, DatabaseUtil.USER,
                DatabaseUtil.PASSWORD, DatabaseUtil.DATABASE)
        self.connection = connection
        
    def close(self):
        """
        Function to close the database connection
        """
        self.connection.close()
        
    
    def getVehicle(self, username):
        """
        Written by: Ching Loo(s3557584)
        
        Task A
        
        Function to display all vehicles the user is renting
        
        Parameters:
			connection(str): username from currently logged in user
		
		Returns:
			vehicleResult(tuple): Result from the excecuted SQL query
        """
        userID = 0
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT userID FROM user WHERE username = (%s)", [(username)])
            results = cursor.fetchall()
            for i in results:
                userID = i[0]
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleID, vehicleBrand, vehicleModel, colour, seats FROM vehicle WHERE userID = (%s)", [(userID)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
    
    def getVehicleModel(self,vehicleId):
        """
        Written by: Ching Loo(s3557584)
        
        Function to get vehicle model from db
        
        
        Parameters:
			vehicleId(int): vehicle id
		
		Returns:
			results(tuple): Result from the excecuted SQL query
        """
        ID = 0
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleModel FROM vehicle WHERE vehicleID = (%s)", [(vehicleId)])
            results = cursor.fetchall()
            return results
            
    def getUsername(self,userid):
        """
        Written by: Ching Loo(s3557584)
        
        Function to get username from db
        
        
        Parameters:
			userid(int): User id
		
		Returns:
			results(tuple): Result from the excecuted SQL query
        """
        userID = 0
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT username FROM user WHERE userID = (%s)", [(userid)])
            results = cursor.fetchall()
            return results
    
    def searchVehicle(self, userInput):
        """
        Written by: Ching Loo(s3557584)
        
        Task A
        
        Search vehicle function
        
        Parameters:
			userInput(str): Keyword from user input
		
		Returns:
			vehicleResult(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicle WHERE vehicleBrand LIKE %s OR vehicleModel LIKE %s OR colour LIKE %s OR seats LIKE %s OR cost LIKE %s", [(userInput), (userInput), (userInput), (userInput), (userInput)])
            vehicleResult = cursor.fetchall()
            return vehicleResult
    
    
    def getLocation(self):
        """
        Written by: Ching Loo(s3557584)
        
        Task B Google Maps API
    
        Get location of every vehicle
        
        Parameters:
            None
		
		Returns:
			vehicleResult(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT latitude, longitude, vehicleModel FROM vehicle")
            vehicleResult = cursor.fetchall()
            return vehicleResult
    
    def searchVehicleID(self,userInput):
        """
        Written by: Jason
        
        Function to get vehicle id from db
        
        
        Parameters:
			userInput(int): vehicle id
		
		Returns:
			vehicleIDResult(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT vehicleID FROM vehicle WHERE vehicleID = %s", [(userInput)])
            vehicleIDResult = cursor.fetchall()
            return vehicleIDResult
     
    def searchUserID(self, username):
        """
        Written by: Jason
        
        Function to get user id from db
        
        
        Parameters:
			username(str): username
		
		Returns:
			result(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT userID FROM user WHERE username = %s", [(username)])
            result = cursor.fetchall()
            return result
            
    def getVehicleStatus(self, vehicle_id):
        """
        Written by: Jason
        
        Function to get vehicle rental status from db
        
        
        Parameters:
			vehicle_id(int): vehicle id
		
		Returns:
			result(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT rentalStatus FROM vehicle WHERE vehicleID = %s",[(vehicle_id)])
            res = cursor.fetchall()
            #convert tuple to int
            result = int(res[0][0])
            return result
    
    def getUserID(self, vehicle_id):
        """
        Written by: Jason
        
        Function to get user_id(foreign key in vehicle table) from db
        
        
        Parameters:
			vehicle_id(int): vehicle id
		
		Returns:
			result(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT UserID FROM vehicle WHERE vehicleID = %s", [(vehicle_id)])
            result = cursor.fetchall()
            return result
            
    def getGCEID(self, vehicle_id):
        """
        Written by: Jason
        
        Function to get google calandar id from db
        
        Parameters:
			vehicle_id(int): vehicle id
		
		Returns:
			result(tuple): Result from the excecuted SQL query
        """
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT google_calendar_id FROM appointments WHERE vehicle_id = %s AND status = 'booked'", [(vehicle_id)])
            result = cursor.fetchall()
            return result
            
    def deleteBooking(self, GCEID):
        """
        Written by: Jason
        
        Function to delete booking and make changes to the status in the db
        
        
        Parameters:
			vehicle_id(int): google calander id
        """
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE google_calendar_id = %s", [(GCEID)])
            self.connection.commit()
            return
    
    def cancelVehicle(self, vehicle_id):
        """
        Written by: Jason
        
        Function to delete booking and make changes to the status in the db
        
        Parameters:
			vehicle_id(int): google calander id
        """
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE vehicle SET rentalStatus = 1, userID = NULL WHERE vehicleID = (%s)", [(vehicle_id)])
            self.connection.commit()
            return        
    
    def updateVehicle(self, userInput):
        """
        Written by: Ching Loo(s3557584)
        
        Task B
    
        Update vehicle table function
    
        Parameters:
            userInput(str): vehicle if from user input
		
        Returns:
            vehicleResult(tuple): Result from the excecuted SQL query
        """
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
        """
        Written by: Jason
        
        Function to book and make changes to the rental status in db
        
        
        Parameters:
			vehicle_id(int): vehicle id
            user_id(int): user id
		
		Returns:
			None
        """
        #update vehicle table
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE vehicle SET rentalStatus = 0, userID = (%s) WHERE vehicleID = (%s)", [(user_id), (vehicle_id)])
            self.connection.commit()
            print("Vehicle Booked!")
            print("")
        return
    
    def getImageName(self, userInput):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT imageName FROM user WHERE username = %s", [(userInput)])
            result = cursor.fetchall()
            return result
