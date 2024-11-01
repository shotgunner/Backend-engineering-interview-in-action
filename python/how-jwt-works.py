
import base64
import json
import hmac
import hashlib
import time
from typing import Dict, Optional

class JWT:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def _base64url_encode(self, data: bytes) -> str:
        """Encode bytes to base64url format"""
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

    def _base64url_decode(self, data: str) -> bytes:
        """Decode base64url format to bytes"""
        padding = '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data + padding)

    def create_token(self, payload: Dict, expires_in: int = 3600) -> str:
        """Create a JWT token"""
        # Header
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        # Add expiration to payload
        payload["exp"] = int(time.time()) + expires_in
        
        # Encode header and payload
        header_encoded = self._base64url_encode(json.dumps(header).encode())
        payload_encoded = self._base64url_encode(json.dumps(payload).encode())
        
        # Create signature
        message = f"{header_encoded}.{payload_encoded}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        signature_encoded = self._base64url_encode(signature)
        
        # Combine all parts
        return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token"""
        try:
            # Split token parts
            header_encoded, payload_encoded, signature_encoded = token.split('.')
            
            # Verify signature
            message = f"{header_encoded}.{payload_encoded}"
            expected_signature = hmac.new(
                self.secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            expected_signature_encoded = self._base64url_encode(expected_signature)
            
            if signature_encoded != expected_signature_encoded:
                return None
                
            # Decode payload
            payload = json.loads(self._base64url_decode(payload_encoded))
            
            # Check expiration
            if payload.get("exp", 0) < time.time():
                return None
                
            return payload
            
        except Exception:
            return None

# Example usage
if __name__ == "__main__":
    # Initialize JWT with a secret key
    jwt = JWT("your-secret-key-here")
    
    # Create a token
    payload = {
        "user_id": 123,
        "username": "john_doe",
        "role": "admin"
    }
    token = jwt.create_token(payload)
    print(f"Generated Token: {token}\n")
    
    # Verify and decode token
    decoded_payload = jwt.verify_token(token)
    print(f"Decoded Payload: {decoded_payload}")
    
    # Example with expired token
    expired_payload = {
        "user_id": 456,
        "exp": int(time.time()) - 3600  # Expired 1 hour ago
    }
    expired_token = jwt.create_token(expired_payload)
    result = jwt.verify_token(expired_token)
    print(f"\nExpired Token Result: {result}")  # Should print None
