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

def get_wallet_balance():
    method = "GET"
    path = "/v2/wallet/balances"
    timestamp = str(int(time.time()))
    
    signature_data = method + timestamp + path
    signature = generate_signature(API_SECRET, signature_data)
    
    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        BASE_URL + path,
        headers=headers,
        timeout=10
    )
    return response.json()

print("Testing Delta API keys...")
result = get_wallet_balance()
print(json.dumps(result, indent=2))