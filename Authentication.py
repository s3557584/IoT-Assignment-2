import MySQLdb

class Authentication:
    #Constructor
    def __init__(self):
        pass
    #Login function
    def Login(self):
		while True:
            #Prompt user input for ID and Password
			username = raw_input("Enter you username: ")
			password = raw_input("Please enter your password:")
			#Connect to database
			dbconn = MySQLdb.connect("35.189.29.67","root","password","IoTAssignment2") or die("could not connect to database")
			cursor = dbconn.cursor()
            #SQL Query for authenticate credentials
			authenticate_user = ("SELECT * FROM users WHERE username = (%s) AND password = (%s)")
			cursor.execute(authenticate_user,[(username),(password)])			
			
            # fetch all of the rows from the query
			results = cursor.fetchall ()
			# If ID and Password matches 
			if results:
				for i in results:
					print("Welcome "+i[2])
                    # Calls the main menu
                    self.Menu()
			else:
				print("Incorrect username or password")
	
    #Main Menu function			
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
