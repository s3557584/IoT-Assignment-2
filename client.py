import socket

host = '123.208.55.187'
port = 10300

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
def unlockCar(choice):
    userChoice = choice
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    data_to_transfer = "{},{},{}".format(userChoice,username,password)

    return data_to_transfer

def returnCar(choice):
    userChoice = choice
    vehicleId = input("Enter Vehicle ID: ")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    data_to_transfer = "{},{},{},{}".format(userChoice,vehicleId,username,password)

    return data_to_transfer

def menu():
        print("************WELCOME**************")
        choice = input("""A: Unlock Car\nB: Return Car\nPlease enter your choice: """)

        if choice == "A" or choice == "a":
            data_to_trasfer = unlockCar(choice)
            if s.send(str.encode(data_to_trasfer)):
                print("Data sent")
            reply = s.recv(1024) 
            print(reply.decode('utf-8'))
            menu()
        elif choice == "B" or choice == "b":
            data_to_trasfer = returnCar(choice)
            if s.send(str.encode(data_to_trasfer)):
                print("Data sent")
            reply = s.recv(1024) 
            print(reply.decode('utf-8'))
            menu()
        else:
            print("You must only select either A or B.")
            print("Please try again")
            menu()
while True:
    menu()
s.close()