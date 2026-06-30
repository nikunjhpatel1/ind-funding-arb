import requests
import json

url = "https://api.india.delta.exchange/v2/products"
response = requests.get(url, timeout=10)
data = response.json()["result"]

print("=== BTC perpetual contracts on Delta India ===")
for product in data:
    if "BTC" in product["symbol"] and product["contract_type"] == "perpetual_futures":
        print(f"Symbol: {product['symbol']:12} | Quote: {product['quoting_asset']['symbol']:5} | Settle: {product['settling_asset']['symbol']}")
