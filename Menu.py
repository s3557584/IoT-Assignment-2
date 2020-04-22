from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
utilsObj = DatabaseUtil()
loginAndRegisterObj = LoginAndRegister()
class Menu:
	
	# Constructor
    def __init__(self):
        pass
        
    # Start function (Entry point of the program)
    def Start(self):
		while True:
			
			# If ID and Password matches
			if loginAndRegisterObj.authenticate() == True:
				
				# Closes the DB connection
				utilsObj.close()
				
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
