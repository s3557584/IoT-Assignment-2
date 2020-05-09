from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib, binascii, os

api = Blueprint("api", __name__)



# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    password = db.Column(db.String(1111))
    vehicle = db.relationship('Vehicle', backref = 'userRenting')
    
    def __init__(self, username, firstname, surname, password):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.password = password

# Vehicle Class/Model
class Vehicle(db.Model):
    vehicleID = db.Column(db.Integer, primary_key=True)
    vehicleBrand = db.Column(db.String(100))
    vehicleModel = db.Column(db.String(100))
    rentalStatus = db.Column(db.Boolean)
    colour = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    location = db.Column(db.String(100))
    cost = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))

    def __init__(self, vehicleBrand, vehicleModel, rentalStatus, colour, seats, location, cost, userID):
        self.vehicleBrand = vehicleBrand
        self.vehicleModel = vehicleModel
        self.rentalStatus = rentalStatus
        self.colour = colour
        self.seats = seats
        self.location = location
        self.cost = cost
        self.userID = userID

# Vehiccle Schema
class VehicleSchema(ma.Schema):
    class Meta:
        fields = ('vehicleID', 'vehicleBrand', 'vehicleModel', 'rentalStatus', 'colour', 'seats', 'location', 'cost', 'userID')

#User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('userID', 'username', 'firstname', 'surname', 'password')
# Init schema
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Create a Vehicle
@api.route('/vehicle', methods=['POST'])
def add_vehicle():
  vehicleBrand = request.json['brand']
  vehicleModel = request.json['model']
  rentalStatus = request.json['status']
  colour = request.json['colour']
  seats = request.json['seats']
  location = request.json['location']
  cost = request.json['cost']
  userID = request.json['id']

  new_vehicle = Vehicle(vehicleBrand, vehicleModel, rentalStatus, userID)

  db.session.add(new_vehicle)
  db.session.commit()

  return vehicle_schema.jsonify(new_vehicle)

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# Create a User
@api.route('/user', methods=['POST'])
def add_user():
  username = request.json['username']
  firstname = request.json['firstname']
  surname = request.json['surname']
  password = hash_password(request.json['password'])

  new_user = User(username, firstname, surname, password)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

# Endpoint to show all people.
@api.route("/user", methods = ["GET"])
def get_users():
    all_Users = User.query.all()
    result = users_schema.dump(all_Users)
    return jsonify(result)

# Get All vehicles
@api.route('/vehicle', methods=["GET"])
def get_vehicles():
  all_vehicles = Vehicle.query.all()
  result = vehicles_schema.dump(all_vehicles)
  return jsonify(result)
