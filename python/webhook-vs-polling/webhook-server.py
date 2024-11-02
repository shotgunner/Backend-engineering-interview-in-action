from flask import Flask, request, jsonify
import requests
import threading
import time
import uuid

app = Flask(__name__)

# Store registered webhooks
webhooks = {}

@app.route('/register', methods=['POST'])
def register_webhook():
    """Register a new webhook callback URL"""
    data = request.get_json()
    
    if 'callback_url' not in data:
        return jsonify({'error': 'callback_url is required'}), 400
        
    # Generate unique ID for this webhook
    webhook_id = str(uuid.uuid4())
    webhooks[webhook_id] = {
        'callback_url': data['callback_url'],
        'status': 'pending'
    }
    
    # Simulate async processing
    def process_webhook():
        time.sleep(5)  # Simulate work
        webhooks[webhook_id]['status'] = 'completed'
        
        # Send webhook callback
        try:
            callback_url = webhooks[webhook_id]['callback_url']
            print(f"Sending webhook to {callback_url}")
            payload = {
                'webhook_id': webhook_id,
                'status': 'completed',
                'message': 'Processing completed successfully'
            }
            requests.post(callback_url, json=payload)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook: {e}")
    
    thread = threading.Thread(target=process_webhook)
    thread.start()
    
    return jsonify({
        'webhook_id': webhook_id,
        'status': 'pending',
        'message': 'Webhook registered successfully'
    })

@app.route('/status/<webhook_id>', methods=['GET']) 
def get_status(webhook_id):
    """Get the current status of a webhook"""
    if webhook_id not in webhooks:
        return jsonify({'error': 'Webhook not found'}), 404
        
    return jsonify({
        'webhook_id': webhook_id,
        'status': webhooks[webhook_id]['status']
    })

if __name__ == '__main__':
    app.run(port=5000)


# how client should call the server
# curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"callback_url": "http://localhost:5001/webhook"}'
# curl http://localhost:5000/status/1234567890