from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
from Book import Book
utilsObj = DatabaseUtil()
loginAndRegisterObj = LoginAndRegister()
bookObj = Book()
class Menu:
	 # Constructor
	def __init__(self):
		pass

	#Function for login    
	def Login(self):
		while True:
			global username 
			username = raw_input("Enter you username: ")
			password = raw_input("Please enter your password:")
			# If ID and Password matches
			if loginAndRegisterObj.authenticate(username, password) == True:
				print("Welcome " + username)
				# Calls the main menu
				self.Menu() 
			else:
				print("Incorrect username or password")
	
	#Function for register
	def Register(self):
		while True:
			#Calls enterUsername() function to take input from user
			username = loginAndRegisterObj.enterUsername()
			#Calls enterName() function to take input from user
			firstname, surname = loginAndRegisterObj.enterName()
			#Calls enterPassword() function to take input from user
			password = loginAndRegisterObj.enterPassword()
			#Encrypting the password taken from user input before storing into database
			encryptedPassword = loginAndRegisterObj.encryptPassword(password)
			#Storing the details to database
			with utilsObj.connection.cursor() as cursor:
				cursor.execute("INSERT INTO user (username,firstname,surname,password) VALUES (%s,%s,%s,%s)", (username,firstname,surname,encryptedPassword))
			utilsObj.connection.commit()
			
			self. Start()
        
	# Start function (Entry point of the program)
	def Start(self):
		print("************IoTAssignment2**************")
		choice = raw_input("""A: Login\nB: Register\nQ: Quit\nPlease enter your choice: """)
		if choice == "A" or choice == "a":
			self.Login()
		elif choice == "B" or choice == "b":
			self.Register()
 
	# Menu function   
	def Menu(self):
		print("************WELCOME**************")
		choice = raw_input("""A: Booked Cars\nB: Search Car\nC: Book a Car\nD: Cancel a Booking\nQ: Quit\nPlease enter your choice: """)

		if choice == "A" or choice == "a":
			print("List of cars you are currently renting")
			getVehicleResult = utilsObj.getVehicle(username)
			for i in getVehicleResult:
				print(i[0]+" "+i[1])
				print("")
			self.Menu()
		elif choice == "B" or choice == "b":
			search = raw_input("Enter Keyword: ")
			searchVehicleResult = utilsObj.searchVehicle(search)
			for i in searchVehicleResult:
				print(i[1]+" "+i[2])
				print("")
			self.Menu()
		elif choice == "C" or choice == "c":
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
			self.Menu()
		elif choice == "D" or choice == "d":
			user_id = utilsObj.searchUserID(username)
			bookObj.cancel_helper(user_id)
			self.Menu()
		elif choice == "Q" or choice == "q":
			utilsObj.close()
			sys.exit
		else:
			print("You must only select either A,B,C,D or E.")
			print("Please try again")
			self.Menu()
