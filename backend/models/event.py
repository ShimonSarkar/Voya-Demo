from models.database import db
from datetime import datetime
from models.trip import Trip

class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey(Trip.id, ondelete='CASCADE'), nullable=False)
    google_event_id = db.Column(db.String(255), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    entity_type = db.Column(db.Enum('flight', 'reservation', name='entity_type'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)