from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

# Set up Flask and database
app = Flask(__name__)

# Set the secret key ( Don't foget to change this to secret key aor random ! for development version)
app.secret_key = 'temporary_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wifis.db')
db = SQLAlchemy(app)

# Set up SocketIO
socketio = SocketIO(app)

# Import routes after the db is initialized to avoid circular import
from routes import *

if __name__ == '__main__':
    # Get host and port from environment variables, use defaults if not provided
    host = os.environ.get('FLASK_HOST', '192.168.1.237')
    port = int(os.environ.get('FLASK_PORT', 5000))

    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the app on the local network interface with debug mode enabled
    socketio.run(app, host=host, port=port, debug=True)



