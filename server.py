import socket
from pushbullet import Pushbullet
from LoginAndRegister import LoginAndRegister
from DatabaseUtil import DatabaseUtil
obj = LoginAndRegister()
objDB_util = DatabaseUtil()
class server:
    """
    Task B
    
    Written by: Ching Loo(s3557584)
    
    Server class for Task B
    """
    
    def __init__(self):
        """
        Empty Constructor
        """
        pass
    
    #Initiate socket
    def setupServer(self, host, port):
        """
        Function to initiate socket
        
        Parameters:
			host(str): host ip address
            port(int): port number
		
		Returns:
			s: Socket binding 
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created.")
        try:
            s.bind((host, port))
        except socket.error as msg:
            print(msg)
        print("Socket bind comlete.")
        return s
    
    def process_data_from_client(self, dataReceived):
        """
        Function to proccess data from client
        
        Parameters:
			dataReceived(str): Data from client
        
        Returns:
            data1 to 4(str): Processed data from client
        """
        count = dataReceived.count(',')
        
        #Checks amount of data recieve from client
        #Split client data to individual variables
        if count == 2:
            data1, data2, data3 = dataReceived.split(",")
            return data1, data2, data3
        elif count == 3:
            data1, data2, data3, data4 = dataReceived.split(",")
            return data1, data2, data3, data4
        elif count == 1:
            data1, data2 = dataReceived.split(",")
            return data1, data2
    
    
    def setupConnection(self, s):
        """
        Looking for client connection and establish connection
        """
        s.listen(1) # Allows one connection at a time.
        conn, address = s.accept()
        print("Connected to: " + address[0] + ":" + str(address[1]))
        return conn
    
    #Unlock Vehicle function
    def unlockVehicle(self, username, password):
        
        #Checks if user id or password is correct or not
        if obj.authenticate(username, password) == True:
            pb = Pushbullet("o.Cj5JI5pc44aSBeGILk4y9ndEBiLzyWUf")
            print(pb.devices)
            dev = pb.get_device('HUAWEI TAS-L29')
            
            #Sends push notification to phone
            push = dev.push_note("NOTICE: ","Vehicle Unlocked!!")
            reply = "Vehicle Unlocked!!"
        
        #If incorrect sends error message
        else:
            reply = "Incorrect Username or Password"
        return reply
    
    #Return Vehicle function
    def returnVehicle(self, vehicleID, username, password):
        if obj.authenticate(username, password) == True:
            print(vehicleID)
            reply = objDB_util.updateVehicle(vehicleID)
            print(reply)
        else:
            reply = "Incorrect Username or Password"
        return reply
    
    #Return Vehicle function
    def unlockVehicleFaceAuth(self, status):
        #Checks if user id or password is correct or not
        if status == 'True':
            pb = Pushbullet("o.Cj5JI5pc44aSBeGILk4y9ndEBiLzyWUf")
            print(pb.devices)
            dev = pb.get_device('HUAWEI TAS-L29')
            
            #Sends push notification to phone
            push = dev.push_note("NOTICE: ","Vehicle Unlocked!!")
            reply = "Vehicle Unlocked!!"
        
        #If incorrect sends error message
        else:
            reply = "Unauthorised"
        return reply
    
    def dataTransfer(self, conn):
        """
        Main functionality of the server
        """
        
        # A big loop that sends/receives data until told not to.
        while True:
            
            # Receive the data
            data = conn.recv(1024) # receive the data from client
            data = data.decode('utf-8')
            count = data.count(',')
            command = " "
            vehicleId = " "
            username = " "
            password = " "
            status = False
            
            if count == 2:
                command, username, password = self.process_data_from_client(data)
            elif count == 3:
                command, vehicleId, username, password = self.process_data_from_client(data)
            elif count == 1:
                command, status = self.process_data_from_client(data)
                
           
            #If user chooses A unlocks vehicle
            if command == 'A' or command == "a":
                
                #Calls the unlock vehicle function
                reply = self.unlockVehicle(username, password)
                encoded_data = reply.encode('utf-8')
                
                #Send the reply back to the client
                conn.sendall(encoded_data)
            
            #If user chooses B unlocks vehicle but with face auth
            elif command == 'B' or command == "b":
                
                #Calls the unlock vehicle function with face auth
                reply = self.unlockVehicleFaceAuth(status)
                encoded_data = reply.encode('utf-8')
                
                #Send the reply back to the client
                conn.sendall(encoded_data)
            
            #If user chooses C return vehicle
            elif command == 'C' or command == "c":
                
                #Calls the return vehicle function
                reply = self.returnVehicle(vehicleId, username, password)
                encoded_data = reply.encode('utf-8')
                
                #Send the reply back to the client
                conn.sendall(encoded_data)
            else:
                reply = 'Unknown Command'
                encoded_data = reply.encode('utf-8')
                
                #Send the reply back to the client
                conn.sendall(encoded_data)
                print("Data has been sent!")
        conn.close()

if __name__ == "__main__":
    #HOST, PORT = "10.0.0.49", 10300
    HOST, PORT = "10.0.0.21", 10400
    serverObj = server()
    s = serverObj.setupServer(HOST, PORT)
    while True:
        conn = serverObj.setupConnection(s)
        serverObj.dataTransfer(conn)
