from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
utilsObj = DatabaseUtil()
loginAndRegisterObj = LoginAndRegister()
class Menu:
	 # Constructor
	def __init__(self):
		pass

	#Function for login    
	def Login(self, username, password):
		status = False
		while True:
			# If ID and Password matches
			if loginAndRegisterObj.authenticate(username, password) == True:
				status = True
				return status
			else:
				print("Incorrect username or password")
				return status
	
	#Function for register
	def Register(self):
		username = ""
		firstname = ""
		surname = ""
		while True:
			username = input("Please enter a username: ")
			#Calls enterUsername() function to take raw_input from user
			if loginAndRegisterObj.enterUsername(username) == True:
				#Calls enterName() function to take raw_input from user
				firstname = input("Enter your first name: ")
				surname = input("Enter your surname: ")
				if loginAndRegisterObj.enterName(firstname, surname) == True:
					#Calls enterPassword() function to take raw_input from user
					password = input("Enter your password\n(Min 6 and Max 20)\n(Must have one number, lowercase, uppercase and special character)\n: ")
					confirmPassword = input("Confirm password: ")
					if loginAndRegisterObj.enterPassword(password, confirmPassword) == True:
						#Encrypting the password taken from user raw_input before storing into database
						encryptedPassword = loginAndRegisterObj.encryptPassword(password)
						#Storing the details to database
						with utilsObj.connection.cursor() as cursor:
							cursor.execute("INSERT INTO user (username,firstname,surname,password) VALUES (%s,%s,%s,%s)", (username,firstname,surname,encryptedPassword))
						utilsObj.connection.commit()
						cursor.close()
						self. Start()
        
	# Start function (Entry point of the program)
	def Start(self):
		print("************IoTAssignment2**************")
		choice = input("A: Login\nB: Register\nQ: Quit\nPlease enter your choice: ")
		if choice == "A" or choice == "a":
			global username 
			username = input("Enter you username: ")
			password = input("Please enter your password:")
			if self.Login(username, password) == True:
				print("Welcome " + username)
				# Calls the main menu
				self.Menu()
			else:
				self.Start()
		elif choice == "B" or choice == "b":
			self.Register()
 
	# Menu function   
	def Menu(self):
		print("************WELCOME**************")
		choice = input("""A: Booked Cars\nB: Search Car\nC: Book a Car\nD: Cancel a Booking\nQ: Quit\nPlease enter your choice: """)

		if choice == "A" or choice == "a":
			print("List of cars you are currently renting")
			getVehicleResult = utilsObj.getVehicle(username)
			for i in getVehicleResult:
				print(i[0]+" "+i[1])
				print("")
			self.Menu()
		elif choice == "B" or choice == "b":
			search = input("Enter Keyword: ")
			searchVehicleResult = utilsObj.searchVehicle(search)
			for i in searchVehicleResult:
				print(i[1]+" "+i[2])
				print("")
			self.Menu()
		elif choice == "C" or choice == "c":
			self.Menu()
		elif choice == "D" or choice == "d":
			self.Menu()
		elif choice == "Q" or choice == "q":
			utilsObj.close()
			Sys.exit
		else:
			print("You must only select either A,B,C,D or E.")
			print("Please try again")
			self.Menu()
