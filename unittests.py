from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
from FaceAuthentication import FaceAuthentication
from Menu import Menu
import unittest
import mock
import socket
from socket import AF_INET, SOCK_STREAM
from mock import patch
import requests
import json

dbUtilObj = DatabaseUtil()
LandRObj = LoginAndRegister()
menuObj = Menu()
faceAuthObj = FaceAuthentication()
class Tests(unittest.TestCase):
    
    """
    Task D: Unit Test
    
    Written by: Ching Loo(s3557584)
    
    This class contains the code for unit tests in this assignment
    """
    
    
    #test_getVehicle is testing the view booked car function    
    def test_getVehicle(self):
        """
        Viewing a user who has not book any cars
        """
        result = dbUtilObj.getVehicle("Testing")
        self.assertFalse(result)

    def test_getVehicle(self):
        """
        Viewing a user who has booked cars
        """ 
        result = dbUtilObj.getVehicle("Ching")
        self.assertTrue(result)
        
    #test_searchVehicle is testing the search vehicle function
    def test_searchVehicle_1(self):
        """
        Search by color
        """
        result = dbUtilObj.searchVehicle("black")
        self.assertTrue(result)
    
    def test_searchVehicle_2(self):
        """
        Search by brand 
        """
        result = dbUtilObj.searchVehicle("Toyota")
        self.assertTrue(result)
    
    def test_searchVehicle_3(self):
        """
        Search by model
        """
        result = dbUtilObj.searchVehicle("Altis")
        self.assertTrue(result)
    
    def test_searchVehicle_4(self):
        """
        Search by number of seats
        """ 
        result = dbUtilObj.searchVehicle(4)
        self.assertTrue(result)
    
    #book_vehicle is testing book vehicle function
    
    #When a user books a car the function will change the renting status of
    #a vehicle to not available for renting
    def book_vehicle_1(self):
        """
        Book a car
        """
        result = dbUtilObj.book(15, 1)
        self.assertTrue(result)
    
    def book_vehicle_2(self):
        """
        Book a already booked car
        """
        result = dbUtilObj.book(15, 1)
        self.assertFalse(result)
    
    def book_vehicle_3(self):
        """
        Book a non existing car
        """
        result = dbUtilObj.book(15, 4)
        self.assertFalse(result)
    
    
    #test_updateVehicle is testing the return vehicle function.
    
    #When a user returns a car the function will change the renting status
    #of a car to available for renting
    def test_updateVehicle(self):
        """
        Returning an already returned vehicle
        """
        result = dbUtilObj.updateVehicle(1)
        self.assertEqual(result, "Vehicle is already returned!!")
    
    def test_updateVehicle(self):
        """
        Entering a non existant vehicle ID
        """
        result = dbUtilObj.updateVehicle(0)
        self.assertEqual(result, "Incorrect vehicle ID")

    def test_updateVehicle(self):
        """
        Returning a vehicle
        """
        result = dbUtilObj.updateVehicle(2)
        self.assertEqual(result, "Vehicle Returned!!")
    

    #Validation for register
    def test_enterUsername_1(self):
        """
        Entering a correct username
        """  
        self.assertTrue(LandRObj.enterUsername("Testing"))
    
    def test_enterUsername_2(self):
        """
        Entering a username that already exists
        """
        result = LandRObj.enterUsername("Ching")
        self.assertFalse(result)
    
    def test_enterUsername_3(self):
        """
        Leaving the input empty
        """
        result = LandRObj.enterUsername("")
        self.assertFalse(result)
    
    def test_enterName_1(self):
        """
        Entering the names correctly
        """
        self.assertTrue(LandRObj.enterName("Unit", "Testing"))
    
    def test_enterName_2(self):
        """
        Leaving the fields blank
        """
        self.assertFalse(LandRObj.enterName("", ""))
    
    def test_enterName_3(self):
        """
        Entering the names using number
        """ 
        self.assertFalse(LandRObj.enterName("123", "123"))
    
    def test_enterName_4(self):
        """
        Entering the names using special characters
        """
        self.assertFalse(LandRObj.enterName("###", "!@#"))
    
    def test_enterPassword_1(self):
        """
        Entering the password fields correctly
        """
        result = LandRObj.enterPassword("Testing@123", "Testing@123")
        self.assertTrue(result)
    
    def test_enterPassword_2(self):
        """
        Entering the password and confirm password diffrently
        """
        result = LandRObj.enterPassword("Testing@123", "Testing123")
        self.assertFalse(result)
        
    def test_enterPassword_3(self):
        """
        Entering the password fields without the correct requirements
        """
        result = LandRObj.enterPassword("incorrect", "incorrect")
        self.assertFalse(result)
    

    #Login Functionality    
    def test_login(self):
        """
        Login with correct credientials
        """
        self.assertTrue(LandRObj.authenticate("Ching","Testing@123"))
    
    def test_login_false(self):
        """
        Login with incorrect credentials
        """
        self.assertFalse(LandRObj.authenticate("Chng","Testing@123"))
    
    
    #RESTful API
    def test_API_GET_Vehicles(self):
        """
        Get Vehicle
        """
        url = "http://127.0.0.1:5000/vehicle"
        response = requests.get(url)
        self.assertTrue(response)
        print(response)
    
    def test_API_GET_Users(self):
        """
        Get User
        """
        url = "http://127.0.0.1:5000/vehicle"
        response = requests.get(url)
        self.assertTrue(response)
        print(response)
    
    def test_API_POST_Vehicles(self):
        """
        Add Vehicle
        """ 
        url = "http://127.0.0.1:5000/vehicle"
        response = requests.post(url, json={'brand':'Honda','colour':'White','cost':15,'latitude':None,'longitude':None,'status':True,'seats':4,'id':None,'model':'CRZ'})
        self.assertTrue(response)
        print(response)
    
        """
        Add User
        """    
    def test_API_POST_Users(self):
        url = "http://127.0.0.1:5000/user"
        response = requests.post(url, json={'username':'Unittesting','firstname':'Unit','surname':'Testing','password':'Test@123', 'imageName':'croppedUnitTest'})
        self.assertTrue(response)
        print(response)
    

    #Google Maps API
    def test_get_vehicle_locations(self):
        """
        Fetch vehicle locations from database
        """
        results = dbUtilObj.getLocation()
        self.assertTrue(results)
    
    
    #Face Authentication
    def test_faceAuth_1(self):
        """
        Authenticate with correct image
        """
        result=faceAuthObj.faceAuthenticate("A", "ching", "Ching")
        self.assertTrue(result)
    
    def test_faceAuth_2(self):
        """
        Authenticate with incorrect image
        """
        result=faceAuthObj.faceAuthenticate("A", "steve", "Ching")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
