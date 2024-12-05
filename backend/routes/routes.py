# Standard Library Imports
from datetime import datetime, timedelta
import os
import requests

# Third-Party Library Imports
from flask import Blueprint, jsonify, request, redirect
from jose import jwt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Application Imports
from models.database import db
from models.ride import Ride, RideReserved
from models.flight import Flight, FlightTaken
from models.hotel import Hotel, HotelBooked
from models.restaurant import Restaurant, RestaurantReserved
from models.user import User, Token
from models.expense import Expense
from models.trip import Trip
from models.event import Event

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_URL = os.getenv("GOOGLE_TOKEN_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

@routes.route('/rides', methods=['GET'])
def get_all_rides():
    """
    Retrieve all rides from the database.
    """
    try:
        # Query all rides
        rides = Ride.query.all()

        # Format the results as a list of dictionaries
        rides_list = [
            {
                "id": ride.id,
                "origin": ride.origin,
                "destination": ride.destination,
                "estimated_cost": str(ride.estimated_cost),
                "provider": ride.provider,
                "created_at": ride.created_at,
                "updated_at": ride.updated_at
            }
            for ride in rides
        ]

        return jsonify(rides=rides_list), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@routes.route('/flights', methods=['GET'])
def get_all_flights():
    """
    Retrieve all flights from the database.
    """
    try:
        # Query all flights
        flights = Flight.query.all()

        # Format the results as a list of dictionaries
        flights_list = [
            {
                "id": flight.id,
                "origin": flight.origin,
                "destination": flight.destination,
                "departure_time": flight.departure_time,
                "arrival_time": flight.arrival_time,
                "cost": str(flight.cost),
                "airline": flight.airline,
                "flight_number": flight.flight_number,
                "created_at": flight.created_at,
                "updated_at": flight.updated_at
            }
            for flight in flights
        ]

        return jsonify(flights=flights_list), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@routes.route('/hotels', methods=['GET'])
def get_all_hotels():
    """
    Retrieve all hotels from the database.
    """
    try:
        # Query all hotels
        hotels = Hotel.query.all()

        # Format the results as a list of dictionaries
        hotels_list = [
            {
                "id": hotel.id,
                "name": hotel.name,
                "address": hotel.address,
                "cost_per_night": str(hotel.cost_per_night),
                "created_at": hotel.created_at,
                "updated_at": hotel.updated_at
            }
            for hotel in hotels
        ]

        return jsonify(hotels=hotels_list), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@routes.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    """
    Retrieve all restaurants from the database.
    """
    try:
        # Query all restaurants
        restaurants = Restaurant.query.all()

        # Format the results as a list of dictionaries
        restaurants_list = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "cost_per_person": str(restaurant.cost_per_person),
                "cuisine": restaurant.cuisine,
                "created_at": restaurant.created_at,
                "updated_at": restaurant.updated_at
            }
            for restaurant in restaurants
        ]

        return jsonify(restaurants=restaurants_list), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@routes.route('/auth/login', methods=['GET'])
def google_login():
    """
    Redirect user to Google OAuth login page.
    """
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile https://www.googleapis.com/auth/calendar.events"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return jsonify({"redirect_url": google_auth_url}), 200

@routes.route('/auth/callback', methods=['GET'])
def google_callback():
    """
    Handle Google OAuth callback, create a user if needed, and issue a JWT.
    """
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    # Step 1: Exchange code for tokens
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=token_data)

    if response.status_code != 200:
        return jsonify({"error": "Failed to exchange authorization code"}), 400

    tokens = response.json()
    id_token_raw = tokens.get("id_token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in")  # Token expiration time in seconds

    if not id_token_raw or not access_token or not refresh_token:
        return jsonify({"error": "Missing tokens in response"}), 400

    # Decode and validate the ID token
    try:
        user_info = id_token.verify_oauth2_token(id_token_raw, google_requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError as e:
        return jsonify({"error": f"Invalid ID token: {str(e)}"}), 400

    email = user_info.get("email")
    name = user_info.get("name")
    google_id = user_info.get("sub")

    if not email or not google_id:
        return jsonify({"error": "Incomplete user info from Google"}), 400

    # Step 2: Check if user exists; if not, create them
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(
            google_id=google_id,
            email=email,
            name=name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(user)
    user.updated_at = datetime.utcnow()
    db.session.commit()

    # Step 3: Generate JWT for internal app use
    jwt_token = create_jwt_token(user)

    # Step 4: Add token entry to database
    token_entry = Token(
        user_id=user.id,
        jwt=jwt_token,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(seconds=expires_in),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(token_entry)
    db.session.commit()

    return jsonify({
        "jwt_token": jwt_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }), 200

def create_jwt_token(user):
    """
    Generate a JWT for the given user.
    """
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

@routes.route('/auth/logout', methods=['POST'])
def logout():
    """
    Invalidate the user's JWT by removing it from the database.
    """
    user_identity = request.get_json()  # Assuming the user's token details are sent in the request
    token_entry = Token.query.filter_by(token=user_identity["token"]).first()
    if token_entry:
        db.session.delete(token_entry)
        db.session.commit()
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"error": "Invalid token"}), 400

@routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a user's details by their ID.
    """
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "email": user.email, "name": user.name, "google_id": user.google_id}), 200
    return jsonify({"error": "User not found"}), 404

@routes.route('/calendar/events', methods=['GET'])
def get_calendar_events():
    """
    Retrieve Google Calendar events for a specified date range.
    """
    # Extract JWT from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

    # Get user from database
    user_id = int(payload.get("sub"))
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve OAuth token from the database
    token_entry = Token.query.filter_by(jwt=token).first()
    if not token_entry:
        return jsonify({"error": "Google OAuth token not found"}), 401

    # Extract date range from query parameters
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        if not start_date or not end_date:
            raise ValueError("Both start_date and end_date are required.")
        start_date = datetime.fromisoformat(start_date).isoformat() + "Z"
        end_date = datetime.fromisoformat(end_date).isoformat() + "Z"
    except ValueError as e:
        return jsonify({"error": "Invalid date format", "details": str(e)}), 400

    # Use Google Calendar API to fetch events
    creds = {
        "token": token_entry.access_token,
        "refresh_token": token_entry.refresh_token,
        "token_uri": GOOGLE_TOKEN_URL,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
    }

    credentials = Credentials(**creds)

    # Refresh token if access_token is expired
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(google_requests.Request())
            # Update the new access_token in the database
            token_entry.access_token = credentials.token
            token_entry.expires_at = datetime.utcnow() + timedelta(seconds=credentials.expiry - datetime.utcnow().timestamp())
            db.session.commit()
        except Exception as e:
            return jsonify({"error": "Failed to refresh access token", "details": str(e)}), 500

    try:
        service = build("calendar", "v3", credentials=credentials)
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        formatted_events = [
            {
                "id": event.get("id"),
                "summary": event.get("summary"),
                "start": event.get("start").get("dateTime", event.get("start").get("date")),
                "end": event.get("end").get("dateTime", event.get("end").get("date")),
            }
            for event in events
        ]

        return jsonify({"events": formatted_events}), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve calendar events", "details": str(e)}), 500

@routes.route('/calendar/events/add', methods=['POST'])
def add_calendar_event():
    """
    Add a new event to the user's Google Calendar and store it in the database.
    """
    # Extract JWT from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

    # Get user from database
    user_id = int(payload.get("sub"))
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve OAuth token from the database
    token_entry = Token.query.filter_by(jwt=token).first()
    if not token_entry or not token_entry.access_token:
        return jsonify({"error": "Google OAuth token not found"}), 401

    # Get event details from the request body
    try:
        event_data = request.json
        trip_id = event_data['trip_id']
        entity_id = event_data['entity_id']
        entity_type = event_data['entity_type']  # 'flight' or 'reservation'
        summary = event_data['summary']
        start_time = event_data['start_time']  # ISO 8601 format
        end_time = event_data['end_time']  # ISO 8601 format
        description = event_data.get('description', '')
        location = event_data.get('location', '')
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    # Use Google Calendar API to add the event
    creds = Credentials(
        token=token_entry.access_token,
        refresh_token=token_entry.refresh_token,
        token_uri=os.getenv('GOOGLE_TOKEN_URL'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    try:
        service = build("calendar", "v3", credentials=creds)
        google_event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "America/New_York"},
            "end": {"dateTime": end_time, "timeZone": "America/New_York"},
        }

        # Insert the event into Google Calendar
        created_event = service.events().insert(calendarId="primary", body=google_event).execute()
        google_event_id = created_event.get("id")

        # Store the event in the database
        new_event = Event(
            trip_id=trip_id,
            google_event_id=google_event_id,
            entity_id=entity_id,
            entity_type=entity_type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event added successfully", "event": created_event}), 200
    except Exception as e:
        return jsonify({"error": "Failed to add event to Google Calendar", "details": str(e)}), 500

@routes.route('/calendar/events/add-multiple', methods=['POST'])
def add_multiple_calendar_events():
    """
    Add multiple events to the user's Google Calendar and store them in the database.
    """
    # Extract JWT from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

    # Get user from database
    user_id = int(payload.get("sub"))
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve OAuth token from the database
    token_entry = Token.query.filter_by(jwt=token).first()
    if not token_entry or not token_entry.access_token:
        return jsonify({"error": "Google OAuth token not found"}), 401

    # Get event details from the request body
    try:
        events_data = request.json.get('events', [])  # Expecting an array of event objects
        if not events_data:
            raise ValueError("No events data provided.")
    except ValueError as e:
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400

    # Use Google Calendar API to add the events
    creds = Credentials(
        token=token_entry.access_token,
        refresh_token=token_entry.refresh_token,
        token_uri=os.getenv('GOOGLE_TOKEN_URL'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    added_events = []
    try:
        service = build("calendar", "v3", credentials=creds)

        for event_data in events_data:
            try:
                trip_id = event_data['trip_id']
                entity_id = event_data['entity_id']
                entity_type = event_data['entity_type']  # 'flight' or 'reservation'
                summary = event_data['summary']
                start_time = event_data['start_time']  # ISO 8601 format
                end_time = event_data['end_time']  # ISO 8601 format
                description = event_data.get('description', '')
                location = event_data.get('location', '')

                google_event = {
                    "summary": summary,
                    "location": location,
                    "description": description,
                    "start": {"dateTime": start_time, "timeZone": "America/New_York"},
                    "end": {"dateTime": end_time, "timeZone": "America/New_York"},
                }

                # Insert the event into Google Calendar
                created_event = service.events().insert(calendarId="primary", body=google_event).execute()
                google_event_id = created_event.get("id")

                # Store the event in the database
                new_event = Event(
                    trip_id=trip_id,
                    google_event_id=google_event_id,
                    entity_id=entity_id,
                    entity_type=entity_type,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.session.add(new_event)
                added_events.append({"google_event_id": google_event_id, "summary": summary})

            except KeyError as e:
                return jsonify({"error": f"Missing required field in event: {str(e)}"}), 400
            except Exception as e:
                return jsonify({"error": f"Failed to add event: {str(e)}"}), 500

        db.session.commit()

        return jsonify({"message": "Events added successfully", "events": added_events}), 200
    except Exception as e:
        return jsonify({"error": "Failed to add events to Google Calendar", "details": str(e)}), 500

@routes.route('/calendar/events/remove', methods=['POST'])
def remove_calendar_events():
    """
    Remove all Google Calendar events within a given time period.
    """
    # Extract JWT from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode JWT
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception as e:
        return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

    # Get user from database
    user_id = int(payload.get("sub"))
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve OAuth token from the database
    token_entry = Token.query.filter_by(jwt=token).first()
    if not token_entry or not token_entry.access_token:
        return jsonify({"error": "Google OAuth token not found"}), 401

    # Get the time period from request body
    try:
        data = request.json
        start_time = data.get("start_time")  # ISO 8601 format
        end_time = data.get("end_time")  # ISO 8601 format
        if not start_time or not end_time:
            raise ValueError("Both start_time and end_time are required.")
        start_time = datetime.fromisoformat(start_time).isoformat() + "Z"
        end_time = datetime.fromisoformat(end_time).isoformat() + "Z"
    except ValueError as e:
        return jsonify({"error": "Invalid date format", "details": str(e)}), 400

    # Set up Google Calendar API credentials
    creds = Credentials(
        token=token_entry.access_token,
        refresh_token=token_entry.refresh_token,
        token_uri=os.getenv('GOOGLE_TOKEN_URL'),
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    )

    try:
        # Build the Google Calendar API service
        service = build("calendar", "v3", credentials=creds)

        # Retrieve events within the time period
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return jsonify({"message": "No events found in the specified time period."}), 200

        # Remove each event
        for event in events:
            service.events().delete(calendarId="primary", eventId=event["id"]).execute()

        return jsonify({"message": f"{len(events)} event(s) removed successfully."}), 200
    except Exception as e:
        return jsonify({"error": "Failed to remove events from Google Calendar", "details": str(e)}), 500
    
@routes.route('/trips', methods=['POST'])
def create_trip():
    """
    Create a new trip.
    """
    data = request.json
    try:
        # Validate input data
        user_id = data.get('user_id')
        name = data.get('name')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not (user_id and name and start_date and end_date):
            return jsonify({"error": "All fields (user_id, name, start_date, end_date) are required"}), 400

        # Convert date strings to date objects
        start_date = datetime.fromisoformat(start_date).date()
        end_date = datetime.fromisoformat(end_date).date()

        # Create the new trip
        new_trip = Trip(
            user_id=user_id,
            name=name,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(new_trip)
        db.session.commit()

        return jsonify({
            "message": "Trip created successfully",
            "trip": {
                "id": new_trip.id,
                "user_id": new_trip.user_id,
                "name": new_trip.name,
                "start_date": str(new_trip.start_date),
                "end_date": str(new_trip.end_date),
                "created_at": str(new_trip.created_at),
                "updated_at": str(new_trip.updated_at),
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
# Add an entry to the Rides_Reserved table
@routes.route('/trips/<int:trip_id>/rides', methods=['POST'])
def add_reserved_ride(trip_id):
    data = request.json
    try:
        new_ride = RideReserved(
            trip_id=trip_id,
            ride_id=data['ride_id'],
            reservation_time=datetime.fromisoformat(data['reservation_time']),
            total_cost=data.get('total_cost')
        )
        db.session.add(new_ride)
        db.session.commit()
        return jsonify({"message": "Ride reserved successfully", "ride": new_ride.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add an entry to the Restaurants_Reserved table
@routes.route('/trips/<int:trip_id>/restaurants', methods=['POST'])
def add_reserved_restaurant(trip_id):
    data = request.json
    try:
        new_restaurant = RestaurantReserved(
            trip_id=trip_id,
            restaurant_id=data['restaurant_id'],
            reservation_time=datetime.fromisoformat(data['reservation_time']),
            total_cost=data.get('total_cost'),
            status=data.get('status', 'reserved')
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify({"message": "Restaurant reserved successfully", "restaurant": new_restaurant.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add an entry to the Hotels_Booked table
@routes.route('/trips/<int:trip_id>/hotels', methods=['POST'])
def add_booked_hotel(trip_id):
    data = request.json
    try:
        new_hotel = HotelBooked(
            trip_id=trip_id,
            hotel_id=data['hotel_id'],
            check_in_date=datetime.fromisoformat(data['check_in_date']).date(),
            check_out_date=datetime.fromisoformat(data['check_out_date']).date(),
            total_cost=data['total_cost'],
            status=data.get('status', 'booked')
        )
        db.session.add(new_hotel)
        db.session.commit()
        return jsonify({"message": "Hotel booked successfully", "hotel": new_hotel.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add an entry to the Flights_Taken table
@routes.route('/trips/<int:trip_id>/flights', methods=['POST'])
def add_taken_flight(trip_id):
    data = request.json
    try:
        new_flight = FlightTaken(
            trip_id=trip_id,
            flight_id=data['flight_id'],
            status=data.get('status', 'scheduled')
        )
        db.session.add(new_flight)
        db.session.commit()
        return jsonify({"message": "Flight added successfully", "flight": new_flight.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Add an entry to the Expenses table
@routes.route('/trips/<int:trip_id>/expenses', methods=['POST'])
def add_expense(trip_id):
    data = request.json
    try:
        new_expense = Expense(
            trip_id=trip_id,
            category=data['category'],
            description=data['description'],
            amount=data['amount']
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"message": "Expense added successfully", "expense": new_expense.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
