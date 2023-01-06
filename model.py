from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app():
    db.create_all()    
    return app

class rides(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("Name", db.String(100), unique = True)
    telNumber = db.Column("TelephoneNumber", db.Integer)
    rideDate = db.Column("Date", db.Integer)
    rideTime = db.Column("Departure Time", db.Time)
    rideFound = db.Column("Ride Found", db.String(1), default=None)

class rides_atl(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("Name", db.String(100), unique = True)
    telNumber = db.Column("TelephoneNumber", db.Integer)
    rideDate = db.Column("Date", db.Integer)
    rideTime = db.Column("Departure Time", db.Time)
    rideFound = db.Column("Ride Found", db.String(1), default=None)
