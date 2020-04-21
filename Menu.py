from DatabaseUtil import DatabaseUtil
import MySQLdb
dbUtilObj = DatabaseUtil()
class Menu:
	
	# Constructor
    def __init__(self):
        pass
        
    # Login function (Entry point of the program)
    def LoginMenu(self):
		while True:
			
			#Prompt user input for ID and Password
			username = raw_input("Enter you username: ")
			password = raw_input("Please enter your password:")
			
			# Calling authenticate function from DatabaseUtil class and stores the result to the variable
			results = dbUtilObj.authenticate(username, password)
			
			# If ID and Password matches
			if results:
				for i in results:
					print("Welcome "+i[2])
					
					# Closes the DB connection
					dbUtilObj.close()
					
					# Calls the main menu
					self.Menu()	
			else:
				print("Incorrect username or password")
	
	# Menu function			
    def Menu(self):
		print("************WELCOME**************")
		choice = raw_input("""A: Booked Cars
B: Available Cars
C: Search Car
D: Book a Car
E: Cancel a Booking
Q: Quit
Please enter your choice: """)

		if choice == "A" or choice == "a":
			print("A")
			self.Menu()
		elif choice == "B" or choice == "b":
			print("B")
			self.Menu()
		elif choice == "C" or choice == "c":
			print("C")
			self.Menu()
		elif choice == "D" or choice == "d":
			print("D")
			self.Menu()
		elif choice == "E" or choice == "e":
			print("E")
			self.Menu()
		elif choice == "Q" or choice == "q":
			sys.exit
		else:
			print("You must only select either A,B,C,D or E.")
			print("Please try again")
			self.Menu()
