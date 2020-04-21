import MySQLdb

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
    
    # Function to authenticate user logging in
    def authenticate(self, username, password):
        with self.connection.cursor() as cursor:
            
            # Executing SQL query to authenticate user
            cursor.execute("SELECT * FROM users WHERE username = (%s) AND password = (%s)", [(username),(password)])
            
            # Return the results fetched from the query
            return cursor.fetchall()
