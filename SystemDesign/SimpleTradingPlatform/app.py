"""
Simple Trading Platform API

This Flask application serves as a backend for a simplified trading platform.
Users can submit buy orders for stocks via a REST API.

Key Components:
- Flask: Used as the web framework to create API endpoints.
- SQLite: A lightweight disk-based database used to store trade records.
- Kafka: A distributed event streaming platform used to publish trade events
           asynchronously. This allows other services (e.g., a matching
           engine, analytics, notifications) to consume these events.

How it Works:
1. The application initializes a connection to an SQLite database (`trading.db`)
   and creates a `trades` table if it doesn't exist.
2. It sets up a Kafka producer to send messages to a 'trades' topic.
3. The `/buy` endpoint (POST request) allows users to place buy orders.
   - It expects a JSON payload with `symbol`, `quantity`, and `price`.
   - A `User-Id` header is required for identifying the user.
   - The application validates the input.
   - If valid, the trade is recorded in the SQLite database.
   - A trade event message is then published to the Kafka 'trades' topic.
   - A success response is returned to the user.
"""
from flask import Flask, request, jsonify
import sqlite3
import json
from kafka import KafkaProducer

app = Flask(__name__)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_db():
    """
    Establishes a connection to the SQLite database.

    The connection is configured to return rows as objects that allow
    access to columns by name (sqlite3.Row).

    Returns:
        sqlite3.Connection: A connection object to the trading.db database.
    """
    conn = sqlite3.connect('trading.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database by creating the 'trades' table if it doesn't already exist.

    This function is typically called once at application startup.
    The 'trades' table schema includes columns for trade ID, user ID, stock symbol,
    quantity, price, and a timestamp.
    """
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

@app.route('/buy', methods=['POST'])
def buy():
    """
    Handles incoming buy order requests.

    It expects a JSON payload with 'symbol', 'quantity', and 'price'.
    A 'User-Id' must be provided in the request headers.

    The function validates the input, records the trade in the SQLite database,
    and publishes a trade event to a Kafka topic named 'trades'.

    Returns:
        flask.Response: A JSON response indicating success (201) or an error
                        (400 for bad request, 401 for missing User-Id, 500 for internal server error).
                        On success, the response includes the details of the executed trade.
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['symbol', 'quantity', 'price']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate data types and values
        if not isinstance(data['quantity'], int) or data['quantity'] <= 0:
            return jsonify({'error': 'Quantity must be a positive integer'}), 400

        if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            return jsonify({'error': 'Price must be a positive number'}), 400

        # Get user ID from headers
        user_id = request.headers.get('User-Id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 401

        db = get_db()
        cursor = db.cursor()

        # Record the trade in the database
        cursor.execute('''
            INSERT INTO trades (user_id, symbol, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (user_id, data['symbol'].upper(), data['quantity'], data['price']))
        db.commit()

        # Create a trade event message
        trade_event = {
            'user_id': user_id,
            'symbol': data['symbol'].upper(),
            'quantity': data['quantity'],
            'price': data['price'],
            'total': data['quantity'] * data['price']
        }

        # Publish the trade event to Kafka
        producer.send('trades', trade_event)
        producer.flush()

        return jsonify({
            'message': 'Trade executed successfully',
            'trade': trade_event
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
