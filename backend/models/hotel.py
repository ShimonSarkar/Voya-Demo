from flask_sqlalchemy import SQLAlchemy
from models.database import db
from datetime import datetime
from models.trip import Trip

class Hotel(db.Model):
    __tablename__ = 'Hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    cost_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HotelBooked(db.Model):
    __tablename__ = 'Hotels_Booked'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey(Hotel.id, ondelete='CASCADE'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('booked', 'canceled', 'completed', name='hotel_status'), default='booked')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)