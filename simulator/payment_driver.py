import asyncio
import random
import json
import time
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

RAZORPAY_ORDER_URL = "https://api.razorpay.com/v1/orders"

PAYMENT_METHODS = ["upi", "card", "netbanking"]

PARTNERS = [
    "Paytm",
    "PhonePe",
    "CRED",
    "SafeGold Direct"
]

DATA_DIR = Path("data")
LOG_FILE = DATA_DIR / "logs.jsonl"


def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    LOG_FILE.touch(exist_ok=True)


def classify_failure(http_status, response_data):
    if http_status == 200:
        return None

    error = response_data.get("error", {})

    return error.get("code") or "api_error"


def recommend_fallback(method, error_code):
    if error_code in ["BAD_REQUEST_ERROR", "GATEWAY_ERROR", "SERVER_ERROR"]:
        if method == "upi":
            return "card"
        elif method == "card":
            return "upi"
        else:
            return "upi"

    return None


async def create_razorpay_order(client, method, partner):
    start = time.perf_counter()

    amount = random.choice([100, 199, 249, 499, 999])

    payload = {
        "amount": amount * 100,
        "currency": "INR",
        "receipt": f"receipt_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
        "notes": {
            "payment_method": method,
            "partner": partner,
            "simulated_user_id": str(random.randint(10000, 99999))
        }
    }

    try:
        response = await client.post(
            RAZORPAY_ORDER_URL,
            json=payload,
            auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
        )

        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        try:
            response_data = response.json()
        except Exception:
            response_data = {}

        http_status = response.status_code
        razorpay_order_id = response_data.get("id")
        razorpay_status = response_data.get("status")

        error_code = classify_failure(http_status, response_data)

        log = {
            "partner": partner,
            "method": method,
            "amount": amount,
            "http_status": http_status,
            "razorpay_order_id": razorpay_order_id,
            "razorpay_status": razorpay_status,
            "status": "success" if http_status == 200 else "failed",
            "latency_ms": latency_ms,
            "error_code": error_code,
            "fallback_recommendation": recommend_fallback(method, error_code),
            "timestamp": time.time()
        }

    except Exception as e:
        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        log = {
            "partner": partner,
            "method": method,
            "amount": amount,
            "http_status": "CLIENT_EXCEPTION",
            "razorpay_order_id": None,
            "razorpay_status": None,
            "status": "failed",
            "latency_ms": latency_ms,
            "error_code": "client_exception",
            "error_description": str(e),
            "fallback_recommendation": recommend_fallback(method, "client_exception"),
            "timestamp": time.time()
        }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")


async def main(total_requests=100, concurrency=20):
    ensure_data_file()

    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency
    )

    async with httpx.AsyncClient(timeout=20, limits=limits) as client:
        tasks = []

        for _ in range(total_requests):
            method = random.choice(PAYMENT_METHODS)
            partner = random.choice(PARTNERS)

            tasks.append(
                create_razorpay_order(client, method, partner)
            )

        await asyncio.gather(*tasks)

    print(f"Simulation complete. {total_requests} requests logged to {LOG_FILE}")


if __name__ == "__main__":
    asyncio.run(main(total_requests=100, concurrency=20))