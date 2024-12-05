from datetime import datetime
from models.database import db
from models.trip import Trip

class Ride(db.Model):
    __tablename__ = 'Rides'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    estimated_cost = db.Column(db.Numeric(10, 2), nullable=False)
    provider = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RideReserved(db.Model):
    __tablename__ = 'Rides_Reserved'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.id, ondelete='CASCADE'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
