import requests
import time
import os
import csv
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()

# ── LOG FILE SETUP ───────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"rates_{datetime.now().strftime('%Y-%m-%d')}.csv"

def write_log(data):
    """Save one rate reading to today's CSV log file."""
    file_exists = LOG_FILE.exists()
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "exchange", "symbol", "mark_price", "funding_rate"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# ── DELTA EXCHANGE ───────────────────────────────────────────
def fetch_delta():
    url = "https://api.india.delta.exchange/v2/tickers/BTCUSD"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        result = r.json().get("result", {})
        return {
            "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "exchange":     "Delta",
            "symbol":       "BTCUSD",
            "mark_price":   float(result.get("mark_price", 0)),
            "funding_rate": float(result.get("funding_rate", 0)),
        }
    except Exception as e:
        print(f"  [ERROR] Delta: {e}")
        return None

# ── PI42 ─────────────────────────────────────────────────────
def fetch_pi42():
    url = "https://api.pi42.com/v1/market/ticker24Hr/BTCINR"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        ticker = r.json().get("data", {})
        return {
            "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "exchange":     "Pi42",
            "symbol":       "BTCINR",
            "mark_price":   float(ticker.get("c", 0)),
            "funding_rate": None,
        }
    except Exception as e:
        print(f"  [ERROR] Pi42: {e}")
        return None

# ── DISPLAY ──────────────────────────────────────────────────
def display(delta, pi42):
    print("\n" + "="*52)
    print(f"  LIVE RATES  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*52)
    if delta:
        print(f"  DELTA  | Mark Price   : ${delta['mark_price']:>12,.2f}")
        print(f"         | Funding Rate : {delta['funding_rate']*100:>10.6f}%")
    else:
        print("  DELTA  | ⚠ No data")
    print("-"*52)
    if pi42:
        print(f"  PI42   | BTC Price    : ₹{pi42['mark_price']:>12,.2f}")
        print(f"         | Funding Rate : {'N/A':>10}")
    else:
        print("  PI42   | ⚠ No data")
    print("="*52)
    print(f"  Log: {LOG_FILE}")

# ── MAIN LOOP ────────────────────────────────────────────────
def main():
    print("\n🚀 Starting funding rate streamer...")
    print(f"   Logging to: {LOG_FILE}")
    print("   Press Ctrl+C to stop\n")

    errors = 0

    while True:
        try:
            delta = fetch_delta()
            pi42  = fetch_pi42()

            # Save to log file
            if delta:
                write_log(delta)
            if pi42:
                write_log(pi42)

            display(delta, pi42)
            errors = 0  # Reset error count on success

        except Exception as e:
            errors += 1
            print(f"  [ERROR] Unexpected: {e} (#{errors})")
            if errors >= 10:
                print("  Too many errors. Stopping.")
                break

        time.sleep(5)

if __name__ == "__main__":
    main()