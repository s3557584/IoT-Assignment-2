"""
Menu Class mainly displays the console based menus needed in Task A
"""
from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
import os
import sys
from Book import Book
utilsObj = DatabaseUtil()
loginAndRegisterObj = LoginAndRegister()
bookObj = Book()
class Menu:
	def __init__(self):
		"""
		Empty constructor
		"""
		pass
   
	def Login(self, username, password):
		"""
		Task A
		
		Written by: Ching Loo(s3557584)
	
		Login function to log exsiting users into the program
		
		Parameters:
			username(str): Username from user input
			password(str): Password from user input
		
		Returns:
			status(boolean): Indicator with true if verified or false if unverified 
		""" 
		status = False
		while True:			
			
			#Calls authenticate function from LoginAndRegister Class.
			#Check if ID and Password matches.
			if loginAndRegisterObj.authenticate(username, password) == True:
				status = True
				return status
			else:
	
			#If ID and Password does not match Prints error message
				print("")
				print("Incorrect username or password!!!")
				print("")
				return status
	
	def Register(self):
		"""
		Task A
		
		Written by: Ching Loo(s3557584)
		
		Register function to register new user
		
		Parameters:
			None
		
		Returns:
			None
		"""
		username = ""
		firstname = ""
		surname = ""
		
		
		#Calls validation functions from LoginAndRegister class to check user inputs.
		while True:
			print("")
			username = input("Please enter a username: ")
			
			#Calls enterUsername() function from LoginAndRegister to check username input from user
			if loginAndRegisterObj.enterUsername(username) == True:
				print("")
				firstname = input("Enter your first name: ")
				surname = input("Enter your surname: ")
				
				#Calls enterName() function from LoginAndRegister to check username input from user
				if loginAndRegisterObj.enterName(firstname, surname) == True:
					print("")
					password = input("Enter your password\n(Min 6 and Max 20)\n(Must have one number, lowercase, uppercase and special character)\n: ")
					print("")
					confirmPassword = input("Confirm password: ")
					
					#Calls enterPassword() function to check password input from user
					if loginAndRegisterObj.enterPassword(password, confirmPassword) == True:
						
						#Encrypting the password taken from user input before storing into database
						encryptedPassword = loginAndRegisterObj.encryptPassword(password)
						
						#Storing the user details to database if everything checks out
						with utilsObj.connection.cursor() as cursor:
							cursor.execute("INSERT INTO user (username,firstname,surname,password) VALUES (%s,%s,%s,%s)", (username,firstname,surname,encryptedPassword))
						utilsObj.connection.commit()
						print("You are registered!!!")
						print("")
						cursor.close()
						self. Start()

	def bookVehicle(self):
		"""
		Task A
		
		Written by: Jason
		
		Book vehicle function
		
		Parameters:
			None
		
		Returns:
			None
		"""
		user_id = utilsObj.searchUserID(username)
		vehicle_id = bookObj.getVehicleFromClient()
		rentable = bookObj.check_rentable(vehicle_id)
		print(rentable)
		if rentable == 1:
			bookObj.book_helper(user_id, vehicle_id)
			#update vehicle status on the database
			utilsObj.book(user_id,vehicle_id)
		else:
			self.Menu()
	
	def Start(self):
		"""
		Task A
		
		Written by: Ching Loo(s3557584)
        
		Start function (Entry point of the program)
		
		Parameters:
			None
		
		Returns:
			None
		"""
		print("************IoTAssignment2**************")
		choice = input("A: Login\nB: Register\nQ: Quit\nPlease enter your choice: ")
		
		#If user chooses A calls Login() function to log the user in
		if choice == "A" or choice == "a":
			global username 
			print("")
			
			username = input("Enter you username: ")
			password = input("Please enter your password:")
			if username != "" and password != "":
				#If username and password matches redirect user to main menu
				if self.Login(username, password) == True:
					print("")
					print("User: " + username)
					
					#Calls the main menu
					self.Menu()
				#Else if username and password incorrect recall the Start() function
				else:
					self.Start()
			else:
				print("")
				print("Username and Password can't be empty")
				print("")
				self.Start()
				
		#If user chooses B calls Register() function		
		elif choice == "B" or choice == "b":
			self.Register()
		
		#Terminates program if user chooses Q 
		elif choice == "Q" or choice == "q":
			sys.exit()
		
		else:
			print("Please enter either A, B or Q")
			self.Start()
	
	def Menu(self):
		"""
		Menu function
		
		Written by: Ching Loo(s3557584) and Jason
	
		Displays the main menu of the program
		
		Parameters:
			None
		
		Returns:
			None
		"""   
		print("************WELCOME**************")
		choice = input("A: Booked Cars\nB: Search Car\nC: Book a Car\nD: Cancel a Booking\nE: Display vehicle locations\nQ: Quit\nPlease enter your choice: ")
		
		
		#Written by Ching Loo(s3557584)
		#Display all rented vehicles
		#If user choose A display all the vehicles that the user rented
		if choice == "A" or choice == "a":
			print("")
			print("List of cars you are currently renting:")
			print("")
			
			#Calls getVehicle() function from DatabaseUtil class to get vehicle data
			getVehicleResult = utilsObj.getVehicle(username)
			
			#If result not empty display all rented cars
			if getVehicleResult:
				print("Search Results:")
				print("ID  BRAND  MODEL COLOUR SEATS")
				for i in getVehicleResult:
					print(" "+str(i[0])+"   "+i[1]+" "+i[2]+" "+i[3]+"   "+str(i[4]))
					print("")
			
			#If result is empty display error message
			else:
				print("You are not renting any cars.")
				print("")
			
			print("")
			self.Menu()
		
		#Written by: Ching Loo(s3557584) 
		#Search vehicle	
		#If user choose B search vehicle based on keyword that user enters
		elif choice == "B" or choice == "b":
			search = input("Enter Keyword: ")
			counter = 0
			
			#Calls searchVehicle() function from DatabaseUtil class
			searchVehicleResult = utilsObj.searchVehicle(search)
			
			print("")
			print("Search Results:")
			print("ID   BRAND  MODEL COLOUR SEATS")
			
			#Display search results
			for i in searchVehicleResult:
				if i[3] == 1:
					print(" "+str(i[0])+"  "+i[1]+"  "+i[2]+"  "+i[4]+"    "+str(i[5]))
					print("")
			print("")
		
			for i in searchVehicleResult:
				if i[3] == 0:
					counter = counter + 1
			
			if len(searchVehicleResult) == counter:
				print("No vehicle available for booking")
				self.Menu()
			else:
				reply = input("Do you want to book a car?: ")
				
				if reply == "Yes" or reply == "yes":
					self.bookVehicle()
					self.Menu()
				else:
					self.Menu()
			
		#Written by: Jason
		#Book a car
		#If user choose C the user can book a vehicle
		elif choice == "C" or choice == "c":
			self.bookVehicle()
			self.Menu()
		
		#Written by: Jason
		#Cancel a booking
		#If user choose D the user can cancel a booking
		elif choice == "D" or choice == "d":
			user_id = utilsObj.searchUserID(username)
			bookObj.cancel_helper(user_id)
			self.Menu()
		
		
		#Written by: Ching Loo(s3557584)
		#Display vehicle locations
		#If user chooses E display all vehicle locations
		elif choice == "E" or choice == "e":
			#Calls and runs googplemaps.py 
			os.system('python3 googlemaps.py')
		
		elif choice == "Q" or choice == "q":
			utilsObj.close()
			sys.exit()
		else:
			print("You must only select either A,B,C,D or E.")
			print("Please try again")
			self.Menu()
