import requests
import hashlib
import hmac
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("DELTA_API_KEY")
API_SECRET = os.getenv("DELTA_API_SECRET")
BASE_URL = "https://api.india.delta.exchange"

def generate_signature(secret, message):
    return hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def cancel_order(order_id, product_id):
    method = "DELETE"
    path = "/v2/orders"
    timestamp = str(int(time.time()))
    
    body = {
        "id": order_id,
        "product_id": product_id
    }
    body_str = json.dumps(body, separators=(",", ":"))
    
    signature_data = method + timestamp + path + body_str
    signature = generate_signature(API_SECRET, signature_data)
    
    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.delete(
        BASE_URL + path,
        headers=headers,
        data=body_str,
        timeout=10
    )
    return response.json()

# Cancel the order we just placed
order_id = 1390619817
product_id = 27

print(f"Cancelling order {order_id}...")
result = cancel_order(order_id, product_id)
print(json.dumps(result, indent=2))