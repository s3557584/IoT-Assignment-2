from DatabaseUtil import DatabaseUtil
from LoginAndRegister import LoginAndRegister
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
class Tests(unittest.TestCase):
    
    """
    This class contains the code for unit tests in this assignment
    """
    
    """
    test_getVehicle is testing the view booked car function
    """
    
    """Viewing a user who has not book any cars"""
    def test_getVehicle(self):
        result = dbUtilObj.getVehicle("Testing")
        self.assertFalse(result)
    """Viewing a user who has booked cars"""    
    def test_getVehicle(self):
        result = dbUtilObj.getVehicle("Ching")
        self.assertTrue(result)
        
    """
    test_searchVehicle is testing the search vehicle function
    """
    
    """Search by color"""
    def test_searchVehicle_1(self):
        result = dbUtilObj.searchVehicle("black")
        self.assertTrue(result)
    
    """Search by brand """
    def test_searchVehicle_2(self):
        result = dbUtilObj.searchVehicle("Toyota")
        self.assertTrue(result)
    
    """Search by model"""
    def test_searchVehicle_3(self):
        result = dbUtilObj.searchVehicle("Altis")
        self.assertTrue(result)
    
    """Search by number of seats"""   
    def test_searchVehicle_4(self):
        result = dbUtilObj.searchVehicle(4)
        self.assertTrue(result)
    
    """
    test_updateVehicle is testing the return vehicle function.
    
    When a user returns a car the function will change the renting status
    of a car to available for renting
    """
    
    """Returning an already returned vehicle"""
    def test_updateVehicle(self):
        result = dbUtilObj.updateVehicle(1)
        self.assertEqual(result, "Vehicle is already returned!!")
    
    """Entering a non existant vehicle ID"""
    def test_updateVehicle(self):
        result = dbUtilObj.updateVehicle(0)
        self.assertEqual(result, "Incorrect vehicle ID")
    
    """Returning a vehicle"""
    def test_updateVehicle(self):
        result = dbUtilObj.updateVehicle(2)
        self.assertEqual(result, "Vehicle Returned!!")
    
    """
    test_encrypt_decryptPassword is testing the encryption,decryption 
    function for password
    """
    
    """Testing the overall encryption and decryption code"""
    def test_encrypt_decryptPassword(self):
        encrypted = LandRObj.encryptPassword("Testing")
        decrypted = LandRObj.decryptPassword(encrypted)
        self.assertEqual(decrypted, "Testing")
    
    """
    Validation for register
    """
    
    """Entering a correct username """   
    def test_enterUsername_1(self):
        self.assertTrue(LandRObj.enterUsername("Testing"))
    
    """Entering a username that already exists"""
    def test_enterUsername_2(self):
        result = LandRObj.enterUsername("Ching")
        self.assertFalse(result)
    
    """Leaving the input empty"""
    def test_enterUsername_3(self):
        result = LandRObj.enterUsername("")
        self.assertFalse(result)
    
    """Entering the names correctly"""
    def test_enterName_1(self):
        self.assertTrue(LandRObj.enterName("Unit", "Testing"))
    
    """Leaving the fields blank"""
    def test_enterName_2(self):
        self.assertFalse(LandRObj.enterName("", ""))
    
    """Entering the names using number"""    
    def test_enterName_3(self):
        self.assertFalse(LandRObj.enterName("123", "123"))
    
    """Entering the names using special characters"""
    def test_enterName_4(self):
        self.assertFalse(LandRObj.enterName("###", "!@#"))
    
    """Entering the password fields correctly"""
    def test_enterPassword_1(self):
        result = LandRObj.enterPassword("Testing@123", "Testing@123")
        self.assertTrue(result)
    
    """Entering the password and confirm password diffrently"""
    def test_enterPassword_2(self):
        result = LandRObj.enterPassword("Testing@123", "Testing123")
        self.assertFalse(result)
        
    """Entering the password fields without the correct requirements"""
    def test_enterPassword_3(self):
        result = LandRObj.enterPassword("incorrect", "incorrect")
        self.assertFalse(result)
    
    """
    Login Functionality
    """
    """Login with correct credientials"""
    def test_login(self):
        self.assertTrue(LandRObj.authenticate("Ching","Testing@123"))
    """Login with incorrect credentials"""
    def test_login_false(self):
        self.assertFalse(LandRObj.authenticate("Chng","Testing@123"))
    
    """
    RESTful API
    """
   
    
    def test_API_POST_Vehicles(self):
        url = "http://127.0.0.1:5000/vehicle"
        response = requests.post(url, json={'brand':'Honda','colour':'White','cost':15,'location':None,'status':True,'seats':4,'id':None,'model':'Civic'})
        self.assertTrue(response)
        print(response)
        
if __name__ == '__main__':
    unittest.main()
