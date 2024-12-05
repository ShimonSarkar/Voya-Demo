from flask_sqlalchemy import SQLAlchemy
from models.database import db
from datetime import datetime
from models.trip import Trip

class Flight(db.Model):
    __tablename__ = 'Flights'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    airline = db.Column(db.String(255), nullable=False)
    flight_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FlightTaken(db.Model):
    __tablename__ = 'Flights_Taken'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey(Flight.id, ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('scheduled', 'delayed', 'canceled', 'completed', name='flight_status'), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)