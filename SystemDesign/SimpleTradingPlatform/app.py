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
    conn = sqlite3.connect('trading.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
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
