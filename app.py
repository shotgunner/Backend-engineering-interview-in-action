from flask import Flask, request
import logging
import time
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import redis
from elasticsearch import Elasticsearch
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

# Initialize connections
redis_client = redis.Redis(host='redis', port=6379)
es_client = Elasticsearch(['http://elasticsearch:9200'])

def get_db_connection():
    return psycopg2.connect(
        dbname="travelapp",
        user="postgres",
        password="postgres",
        host="db"
    )

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    start_time = time.time()
    
    # Simulate some work and generate logs
    sleep_time = random.uniform(0.1, 0.5)
    time.sleep(sleep_time)
    
    # Log the request
    logger.info(f'Home page accessed. Processing time: {sleep_time:.2f} seconds')
    
    # Record request latency
    REQUEST_LATENCY.observe(time.time() - start_time)
    
    return 'Hello World!'

@app.route('/error')
def error():
    logger.error('This is a sample error!')
    return 'Error generated', 500

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        logger.info('Database connection successful')
        cur.close()
        conn.close()
        return 'DB Connection OK'
    except Exception as e:
        logger.error(f'Database error: {str(e)}')
        return 'DB Connection Failed', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
