import os
import pickle
import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendar():
	
	SCOPES = ['https://www.googleapis.com/auth/calendar']
	
	def __init__(self):
		creds = None
		if os.path.exists('token.pickle'):
			with open('token.pickle', 'rb') as token:
				creds = pickle.load(token)
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
				creds = flow.run_local_server()
			with open('token.pickle', 'wb') as token:
				pickle.dump(creds,token, protocol=2)
				
		self.service = build('calendar', 'v3', credentials = creds)
				
				
		
	def add_event(self, user_id, vehicle_id, start_date, end_date):
		timezone = 'Australia/Melbourne'
		date_format = '%Y-%m-%d'
		event = {
            'summary': "Rent by: " + str(user_id),
            'description': str(user_id) + " renting: " + str(vehicle_id),
            'start': {'date': start_date.strftime(date_format),
                      'timeZone': timezone},
            'end': {'date': end_date.strftime(date_format), 'timeZone': timezone},
        }
		event = self.service.events().insert(calendarId='primary',body=event).execute()
		return event.get('id')
    
        
	def remove_event(self, event_id):
		self.service.events().delete(calendarId='primary' , eventId = event_id).execute()
		
		
