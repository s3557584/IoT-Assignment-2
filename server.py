import socket
from pushbullet import Pushbullet
from LoginAndRegister import LoginAndRegister
from DatabaseUtil import DatabaseUtil
obj = LoginAndRegister()
objDB_util = DatabaseUtil()
class server:
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    #Constructor
    def __init__(self):
        pass
    
    #Initiate socket
    def setupServer(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created.")
        try:
            s.bind((host, port))
        except socket.error as msg:
            print(msg)
        print("Socket bind comlete.")
        return s
    
    #Function to proccess data from client
    def process_data_from_client(self, dataReceived):
        count = dataReceived.count(',')
        if count == 2:
            data1, data2, data3 = dataReceived.split(",")
            return data1, data2, data3
        else:
            data1, data2, data3, data4 = dataReceived.split(",")
            return data1, data2, data3, data4
    
    #Looking for client connection and establish connection
    def setupConnection(self, s):
        s.listen(1) # Allows one connection at a time.
        conn, address = s.accept()
        print("Connected to: " + address[0] + ":" + str(address[1]))
        return conn
    
    #Unlock Vehicle function
    def unlockVehicle(self, username, password):
        if obj.authenticate(username, password) == True:
            pb = Pushbullet("o.Cj5JI5pc44aSBeGILk4y9ndEBiLzyWUf")
            print(pb.devices)
            dev = pb.get_device('HUAWEI TAS-L29')
            push = dev.push_note("NOTICE: ","Vehicle Unlocked!!")
            reply = "Vehicle Unlocked!!"
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
    
    #Main functionality of the server
    def dataTransfer(self, conn):
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
            
            if count == 2:
                command, username, password = self.process_data_from_client(data)
            else:
                command, vehicleId, username, password = self.process_data_from_client(data)
            
            if command == 'A' or command == "a":
                #Calls the unlock vehicle function
                reply = self.unlockVehicle(username, password)
                encoded_data = reply.encode('utf-8')
                conn.sendall(encoded_data)
            elif command == 'B' or command == "b":
                #Calls the return vehicle function
                reply = self.returnVehicle(vehicleId, username, password)
                encoded_data = reply.encode('utf-8')
                conn.sendall(encoded_data)
            else:
                reply = 'Unknown Command'
                encoded_data = reply.encode('utf-8')
                conn.sendall(encoded_data)
                print("Data has been sent!")
            # Send the reply back to the client
        conn.close()

if __name__ == "__main__":
    HOST, PORT = "10.0.0.49", 10300
    serverObj = server()
    s = serverObj.setupServer(HOST, PORT)
    while True:
        conn = serverObj.setupConnection(s)
        serverObj.dataTransfer(conn)
