from DatabaseUtil import DatabaseUtil
utilsObj = DatabaseUtil()
import datetime
from GoogleCalendar import GoogleCalendar
import datefinder


class Book:
	
	def __init__(self):
		
		self.gc = GoogleCalendar()
	
	#this is to check if vehicle exists
	def getVehicleFromClient(self):
		
		while True:
			response = int(raw_input("Please enter Id of vehicle that you wish to book: "))
			#check if vehicle exists
			result = utilsObj.searchVehicleID(response)
			if result:
				return response
				break
			else:
				print("Vehicle not found, please try again")
	
	def check_rentable(self, vehicle_id):
		rentable = utilsObj.getVehicleStatus(vehicle_id)
		
		if rentable == 1:
			return 1
		elif rentable == 0:
			print("Vehicle is not available for rental")
			return 0
		
					
				
	def book_helper(self, user_id, vehicle_id):
		print("When do you want to book")
		start_input = str(raw_input('Please enter the date in dd/mm/yyyy format): '))
		start_date = datetime.datetime.strptime(start_input, '%d/%m/%Y')
		print("When do you want to return")
		return_input = str(raw_input('Please enter the date in dd/mm/yyyy format): '))
		return_date = datetime.datetime.strptime(return_input, '%d/%m/%Y')
		event_id = self.gc.add_event(user_id, vehicle_id, start_date, return_date)
		print("Google Calendar event created")
		status = "booked"
		with utilsObj.connection.cursor() as cursor:
			cursor.execute("INSERT INTO appointments (user_id,vehicle_id,google_calendar_id,start_date,return_date, status) VALUES (%s,%s,%s,%s,%s,%s)", (user_id,vehicle_id,event_id,start_date,return_date,status))
			utilsObj.connection.commit()
		return event_id
		
	def cancel_helper(self, user_id):
		while True:
			vehicle_id = int(raw_input('Enter the vehicle id of the vehicle that you wish to cancel'))
			exists = utilsObj.searchVehicleID(vehicle_id)
			if exists:
				cancelable = utilsObj.getVehicleStatus(vehicle_id)
				if cancelable == 1:
					print("Vehicle is not currently booked")
				else:
					id_matching = utilsObj.getUserID(vehicle_id)
					if id_matching != user_id:
						print("This vehicle is not currently booked by you")
					else:
						google_calendar_id = utilsObj.getGCEID(vehicle_id)
						utilsObj.deleteBooking(google_calendar_id)
						utilsObj.cancelVehicle(vehicle_id)
						convert_id_into_str = str(google_calendar_id)
						event_id = convert_id_into_str[3:-5]
						self.gc.remove_event(event_id)
				break
			else:
				print("Try again")