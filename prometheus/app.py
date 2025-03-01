from flask import Flask
from prometheus_client import Counter, Gauge, push_to_gateway, start_http_server

app = Flask(__name__)

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total app requests')
ACTIVE_USERS = Gauge('app_active_users', 'Number of active users')

@app.route('/')
def index():
    REQUEST_COUNT.inc()
    ACTIVE_USERS.set(10)  # Example: set active users to 10
    
    # Push metrics to Prometheus Pushgateway
    push_to_gateway('localhost:9090', job='flask_app', registry=None)
    
    return "Hello, metrics pushed to Prometheus!"

if __name__ == '__main__':
    app.run(port=5000)
