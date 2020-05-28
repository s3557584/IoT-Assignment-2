"""
Task A: RESTful API

Written by: Ching Loo(s3557584)

Main file of the API
"""
from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import hashlib, binascii, os

api = Blueprint("api", __name__)



# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

class User(db.Model):
    """
    User Class/Model
    """
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    password = db.Column(db.String(1111))
    imageName = db.Column(db.String(100))
    vehicle = db.relationship('Vehicle', backref = 'userRenting')
    
    def __init__(self, username, firstname, surname, password, imageName):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.password = password
        self.imageName = imageName

class Vehicle(db.Model):
    """
    Vehicle Class/Model
    """
    vehicleID = db.Column(db.Integer, primary_key=True)
    vehicleBrand = db.Column(db.String(100))
    vehicleModel = db.Column(db.String(100))
    rentalStatus = db.Column(db.Boolean)
    colour = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    cost = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))

    def __init__(self, vehicleBrand, vehicleModel, rentalStatus, colour, seats, latitude, longitude, cost, userID):
        self.vehicleBrand = vehicleBrand
        self.vehicleModel = vehicleModel
        self.rentalStatus = rentalStatus
        self.colour = colour
        self.seats = seats
        self.latitude = latitude
        self.longitude = longitude
        self.cost = cost
        self.userID = userID

class VehicleSchema(ma.Schema):
    """
    Vehicle Schema class
    """
    class Meta:
        fields = ('vehicleID', 'vehicleBrand', 'vehicleModel', 'rentalStatus', 'colour', 'seats', 'latitude', 'longitude', 'cost', 'userID')

class UserSchema(ma.Schema):
    """
    User Schema
    """
    class Meta:
        fields = ('userID', 'username', 'firstname', 'surname', 'password', 'imageName')
# Init schema
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a Vehicle
@api.route('/vehicle', methods=['POST'])
def add_vehicle():
    """
    Function to add a Vehicle
    
    Parameters:
        None
		
    Returns:
        vehicle_schema.jsonify(new_vehicle): convert received data to json format
    """
    vehicleBrand = request.json['brand']
    vehicleModel = request.json['model']
    rentalStatus = request.json['status']
    colour = request.json['colour']
    seats = request.json['seats']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    cost = request.json['cost']
    userID = request.json['id']

    new_vehicle = Vehicle(vehicleBrand, vehicleModel, rentalStatus, colour, seats, latitude, longitude, cost, userID)

    db.session.add(new_vehicle)
    db.session.commit()

    return vehicle_schema.jsonify(new_vehicle)

#Generate key for password encryption
def generate_key():
    """
    Function to generate key for password encryption
    
    Parameters:
        None
    
    Returns:
        Key: The key used for encryption
    """
    password = b"password"
    salt = b'Oy\nK5o\x15\xa8ex2U\x94A\xb9\x8c'
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

#Encrypt password        
def encryptPassword(password):
    """
    Function to encrypt password before posting it to database
    
    Parameters:
        password(str): password entered by user
        
    Returns:
        encrypted(bytes): Encrypted password
    """
    f = Fernet(generate_key())
    encrypted = f.encrypt(password.encode('utf-8'))
    return encrypted

# Create a User
@api.route('/user', methods=['POST'])
def add_user():
    """
    Function to add a user
    
    Parameters:
			None
		
    Returns:
			vehicle_schema.jsonify(new_vehicle): convert received data to json format
    """
    username = request.json['username']
    firstname = request.json['firstname']
    surname = request.json['surname']
    password = request.json['password']
    imageName = request.json['imageName']
    
    encryptedPassword = encryptPassword(password)

    new_user = User(username, firstname, surname, encryptedPassword, imageName)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Endpoint to show all users.
@api.route("/user", methods = ["GET"])
def get_users():
    """
    Function to show all users
    
    Parameters:
        None
        
    Returns:
        result:Results from database and converts them to json
    """
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)
    return jsonify(result)

# Endpoint to show all vehicles
@api.route('/vehicle', methods=["GET"])
def get_vehicles():
    """
    Function to show all users
    
    Parameters:
        None
        
    Returns:
        result: Results from database and converts them to json
    """
    all_vehicles = Vehicle.query.all()
    result = vehicles_schema.dump(all_vehicles)
    return jsonify(result)
