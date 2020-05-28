"""
Written by: Ching Loo(s3557584)

Client part for Task B
"""
import socket
from FaceAuthentication import FaceAuthentication

obj = FaceAuthentication()

host = '123.208.55.187'
#port = 10300
port = 10400

"""
Connects to server
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def unlockCar(choice, username, password):
    """
    Function to process data for unlock car before sending it to server
    """
    data_to_transfer = "{},{},{}".format(choice,username,password)

    return data_to_transfer

def unlockCarFaceAuth(choice, status):
    """
    Function to process data for unlock car before sending it to server
    """
    data_to_transfer = "{},{}".format(choice,status)

    return data_to_transfer

def returnCar(choice, vehicleId, username, password):
    """
    Function to process data for return car before sending it to server
    """
    data_to_transfer = "{},{},{},{}".format(choice,vehicleId,username,password)

    return data_to_transfer


def menu():
    """
    Main menu for client part
    """
    print("************WELCOME**************")
    choice = input("""A: Unlock Car(Username & Password)\nB: Unlock Car(Facial recognition)\nC: Return Car\nPlease enter your choice: """)
        
    #If user chooses A client takes username and password
    #And sends both of them to server for validation to unlock car 
    if choice == "A" or choice == "a":
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        data_to_trasfer = unlockCar(choice, username, password)
        
        #Sends data to server
        if s.send(str.encode(data_to_trasfer)):
            print("Data sent")
            
            #Receives reply from server
            reply = s.recv(1024) 
            print(reply.decode('utf-8'))
            
            #Calls back main menu
            menu()
    
    elif choice == "B" or choice == "b":
        status = False
        userInput = input("A: Use image or B: use a camera?: ")
        if userInput == "A" or userInput == "a":
            username = input("Enter Username: ")
            imgName = input("Name of the image: ")
            if obj.faceAuthenticate(userInput, imgName, username) == True:
                status = True
            else:
                print("Error: something went wrong (client A)")
                menu()
        elif userInput == "B" or userInput == "b":
            username = input("Enter Username: ")
            imgName = "None"
            if obj.faceAuthenticate(userInput, imgName, username) == True:
                status = True
            else:
                print("Error: something went wrong (client B)")
                menu()
            
        data_to_trasfer = unlockCarFaceAuth(choice, status)
        
        #Sends data to server
        if s.send(str.encode(data_to_trasfer)):
            print("Data sent")
            
            #Receives reply from server
            reply = s.recv(1024) 
            print(reply.decode('utf-8'))
            
            #Calls back main menu
            menu()
    
    #If user chooses B clients takes username ,password and vehicle ID.
    #And sends them to server for validation to return car
    elif choice == "C" or choice == "c":
        vehicleId = input("Enter Vehicle ID: ")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        data_to_trasfer = returnCar(choice, vehicleId, username, password)
            
        #Sends the data to server for validation and change status of vehicle
        if s.send(str.encode(data_to_trasfer)):
            print("Data sent")
            
            #Receives reply from server
            reply = s.recv(1024) 
            print(reply.decode('utf-8'))
            
            #Calls back main menu
            menu()
        else:
            print("You must only select either A or B.")
            print("Please try again")
            menu()
while True:
    menu()
s.close()
