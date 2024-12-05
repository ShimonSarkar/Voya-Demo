from flask_sqlalchemy import SQLAlchemy
from models.database import db
from datetime import datetime
from models.trip import Trip

class Restaurant(db.Model):
    __tablename__ = 'Restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    cost_per_person = db.Column(db.Numeric(10, 2), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RestaurantReserved(db.Model):
    __tablename__ = 'Restaurants_Reserved'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id, ondelete='CASCADE'), nullable=False)
    reservation_time = db.Column(db.DateTime, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2))
    status = db.Column(db.Enum('reserved', 'canceled', 'completed', name='reservation_status'), default='reserved')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)