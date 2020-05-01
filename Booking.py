from DatabaseUtil import DatabaseUtil
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

utilsObj = DatabaseUtil()
class Booking:
    def makeBooking():
        #connecting to database
        with utilsObj.connection.cursor() as db:
                cursor = db.cursor()
        print()
        for Num,Name,Price in treatmentlist: 
            print(Num,Name,"=",Price)
        print()
    
    validtreatment = False
    while validtreatment == False:
        try:
            treatmentchoice = input("Which treatment would you like to book? Please choose a number from the list above: ")
            if treatmentchoice == "quit" or treatmentchoice == "Quit" or treatmentchoice == "QUIT":
                return
            elif int(treatmentchoice) < 1 or int(treatmentchoice) > 27:
                 print("This number is not on the list.")
            else:
                treatment = treatmentlist[int(treatmentchoice) - 1]
                validtreatment = True
        except:
            print("Please enter a valid number.")

            
    print()
    print("Here are the available booking dates")
    print()
    for Num,Day in weekdays: 
        print(Num,Day)
    print()
    
    validday = False
    while validday == False:
        try:
            daychoice = input("Which day is best for you? ")
            if daychoice == "quit" or daychoice == "Quit" or daychoice == "QUIT":
                return
            elif int(daychoice) < 1 or int(daychoice) > 7:
                 print("This number is not on the list.")
            else:
                weekday = weekdays[int(daychoice) - 1]
                validday = True
        except:
            print("Please enter a valid number.")

            
    if str(weekday[1]) == "Monday":
        whichdates = mondaydates
    elif str(weekday[1]) == "Tuesday":
        whichdates = tuesdaydates
    elif str(weekday[1]) == "Wednesday":
        whichdates = wednesdaydates
    elif str(weekday[1]) == "Thursday":
        whichdates = thursdaydates
    elif str(weekday[1]) == "Friday":
        whichdates = fridaydates
    elif str(weekday[1]) == "Saturday":
        whichdates = saturdaydates
    elif str(weekday[1]) == "Sunday":
        whichdates = sundaydates

        
    print()
    print("Here are the dates for " , str(weekday[1]))
    print()
    
    for Num,Day in whichdates: 
        print(Num,Day)
    print()
    
    validdate = False
    while validdate == False:
        try:
            datechoice = input("Which date would suit you best? ")
            if datechoice == "quit" or datechoice == "Quit" or datechoice == "QUIT":
                return
            elif int(datechoice) < 1 or int(datechoice) > 7:
                 print("This number is not on the list.")
            else:
                date = whichdates[int(datechoice) - 1]
                validdate = True
        except:
            print("Please enter a valid number.")

            
    print()
    print("Here are the times for " , str(weekday[1]),"," , str(date[1]))
    print()
    
    for Num,Time in times: 
        print(Num,Time)
    print()
    validtime = False
    while validtime == False:
        try:
            timechoice = input("Which time would you like? ")
            if timechoice == "quit" or timechoice == "Quit" or timechoice == "QUIT":
                return
            elif int(timechoice) < 1 or int(timechoice) > 15:
                 print("This number is not on the list.")
            else:
                time = times[int(timechoice) - 1]
                booktest = (str(date[1]), str(time[1]))
                if booktest in booktestlist:
                    print("Sorry, someone has already taken that time.")
                    validtime = False
                else:
                    validtime = True
        except:
            print("Please enter the number of the time you would like.")    

    validemail = False
    while validemail == False:
        try:
            email = input("Please enter your email address so that I can contact you: ")
            if "@" not in email:
                print("This is not a valid email.")
            else:
                validemail = True
        except:
            print("Please try again.")

    booking = (name , str(treatment[1]) , str(weekday[1]) , str(date[1]) , str(time[1]) , email)

    confirmedbook = False
    while confirmedbook == False:
        try:
            print("Here is your booking:")
            print(booking)
            confirm = input("Is this booking correct? Please confirm. Y/N ")
            if confirm == "N" or confirm == "n" or confirm == "No" or confirm == "NO" or confirm == "no":
                return
            elif confirm == "Y" or confirm == "y" or confirm == "Yes" or confirm == "YES" or confirm == "yes":
                confirmedbook = True
                booktestlist.append(booktest)
                if booking not in bookings:
                    bookings.append(booking)
                    duplicatelist.append(booking)
                else:
                    print("That seems to be a duplicate.")
            else:
                print("That isn't a valid answer.")
                continue
        except:
            print()

    showBookings()

def endAnswer():
    ValidEndAnswer = False
    while ValidEndAnswer == False:
        endquestion = input("Would you like to make another booking? Y/N ")
        if endquestion == "N" or endquestion == "n" or endquestion == "No" or endquestion == "NO" or endquestion == "no":
            raise SystemExit()
        elif endquestion == "Y" or endquestion == "y" or endquestion == "Yes" or endquestion == "YES" or endquestion == "yes":
            ValidEndAnswer = True
        else:
            print("That isn't a valid answer.")
            continue
            
def showBookings():
    print()
    print("Here are the current bookings:")
    count = 0
    while count < len(bookings):
        print(bookings[count])
        count = count + 1
    if len(bookings) == 0:
        print("No bookings currently set.")
        print()
        
    