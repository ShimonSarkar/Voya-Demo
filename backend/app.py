from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models.database import configure_database, db
from routes.routes import routes

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the database
configure_database(app)

# Register the routes
app.register_blueprint(routes)

# Debugging
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initial route
@app.route('/')
def home():
    return jsonify(message="Backend up and running!")

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run(host='localhost', port=5001, debug=True)
