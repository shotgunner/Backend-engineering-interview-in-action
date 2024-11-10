from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

def get_db():
    conn = sqlite3.connect('trips.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create trip endpoint
@app.route('/api/trips', methods=['POST'])
@limiter.limit("5 per minute")  # Stricter limit for creation
def create_trip():
    try:
        data = request.get_json()
        
        # Input validation
        required_fields = ['origin', 'destination', 'date', 'seats_available']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validate date format
        try:
            trip_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
        if data['seats_available'] < 1:
            return jsonify({'error': 'Must have at least one seat available'}), 400

        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            INSERT INTO trips (origin, destination, date, seats_available, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['origin'], data['destination'], data['date'], 
              data['seats_available'], request.headers.get('User-Id')))
        
        trip_id = cursor.lastrowid
        db.commit()
        
        return jsonify({'trip_id': trip_id, 'message': 'Trip created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db' in locals():
            db.close()

# Search trips endpoint
@app.route('/api/trips', methods=['GET'])
def search_trips():
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        date = request.args.get('date')
        
        if not all([origin, destination, date]):
            return jsonify({'error': 'Missing search parameters'}), 400
            
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * FROM trips 
            WHERE origin = ? 
            AND destination = ? 
            AND date = ?
            AND seats_available > 0
        ''', (origin, destination, date))
        
        trips = [dict(row) for row in cursor.fetchall()]
        return jsonify({'trips': trips}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db' in locals():
            db.close()

# Join trip endpoint
@app.route('/api/trips/<int:trip_id>/join', methods=['POST'])
@limiter.limit("3 per minute")  # Prevent rapid booking attempts
def join_trip(trip_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if trip exists and has available seats
        cursor.execute('SELECT seats_available FROM trips WHERE id = ?', (trip_id,))
        trip = cursor.fetchone()
        
        if not trip:
            return jsonify({'error': 'Trip not found'}), 404
        
        if trip['seats_available'] < 1:
            return jsonify({'error': 'No seats available'}), 400
            
        # Update seats and create booking in transaction
        cursor.execute('BEGIN TRANSACTION')
        cursor.execute('''
            UPDATE trips 
            SET seats_available = seats_available - 1 
            WHERE id = ?
        ''', (trip_id,))
        
        cursor.execute('''
            INSERT INTO bookings (trip_id, user_id, booking_date)
            VALUES (?, ?, datetime('now'))
        ''', (trip_id, request.headers.get('User-Id')))
        
        db.commit()
        return jsonify({'message': 'Successfully joined trip'}), 200
        
    except Exception as e:
        if 'db' in locals():
            db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db' in locals():
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
