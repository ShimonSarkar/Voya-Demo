from flask_sqlalchemy import SQLAlchemy
from models.database import db
from datetime import datetime
from models.trip import Trip

class Expense(db.Model):
    __tablename__ = 'Expenses'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    category = db.Column(db.Enum('flight', 'hotel', 'meal', 'transport', name='expense_category'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)