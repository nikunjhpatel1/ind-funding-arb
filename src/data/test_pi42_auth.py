import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("PI42_API_KEY")
API_SECRET = os.getenv("PI42_API_SECRET")
BASE_URL = "https://fapi.pi42.com"

endpoint = "/v1/wallet/futures-wallet/details"
timestamp = str(int(time.time() * 1000))

params = {"timestamp": timestamp}
query_string = urlencode(params)

signature = hmac.new(
    API_SECRET.encode("utf-8"),
    query_string.encode("utf-8"),
    hashlib.sha256
).hexdigest()

url = f"{BASE_URL}{endpoint}?{query_string}"
headers = {
    "api-key": API_KEY,
    "signature": signature,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Origin": "https://pi42.com",
    "Referer": "https://pi42.com/",
    "Accept": "application/json"
}

print(f"URL: {url}")

response = requests.get(url, headers=headers, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Raw Response Text: {response.text[:500]}")