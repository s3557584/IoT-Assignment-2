'''
Task B

Written By: Ching(s3557584) and Lin

A Web application that shows Google Maps around vehicles, using
the Flask framework, and the Google Maps API.
'''
import webbrowser
from threading import Timer
from flask import Flask, render_template, abort
from DatabaseUtil import DatabaseUtil

app = Flask(__name__)


class Vehicle:
    """
    Vehicle Class.
    
    Fetch vehicle locations from database and stores it in a list 
    """
    obj = DatabaseUtil() 
    
    #Calls getLocation() function from DatabaseAndUtil class
    #Fetches the vehicle locations
    results = obj.getLocation()
    
    #Converts result to a 2d list
    latlng = [list(item) for item in results]

@app.route("/")
def show_vehicle():
    """
    Function that takes the data from Vehicle class and passes them to the html template
    """
    vehicle = Vehicle()
    
    if vehicle:
        return render_template('map.html', vehicle=vehicle)
    else:
        abort(404)

def open_browser():
    """
    Function to open browser when launched
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
      Timer(1, open_browser).start();
      app.run(port=5000)
