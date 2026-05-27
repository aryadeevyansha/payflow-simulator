import asyncio
import random
import json
import time
import httpx

PAYMENT_METHODS = ["upi", "card", "netbanking"]

PARTNERS = [
    "Paytm",
    "PhonePe",
    "CRED",
    "SafeGold Direct"
]

async def simulate_payment(client, method, partner):

    start = time.time()

    await asyncio.sleep(random.uniform(0.2, 1.5))

    latency = (time.time() - start) * 1000

    failure_probability = {
        "upi": 0.12,
        "card": 0.05,
        "netbanking": 0.08
    }

    status = (
        "failed"
        if random.random() < failure_probability[method]
        else "success"
    )

    error_code = None
    retry_attempted = False
    recovered_after_retry = False

    if status == "failed":

        error_code = random.choice([
            "bank_timeout",
            "network_error",
            "authentication_failed"
        ])

        if error_code in ["bank_timeout", "network_error"]:

            retry_attempted = True

            retry_success = random.random() < 0.6

            if retry_success:
                status = "success"
                recovered_after_retry = True

    log = {
        "partner": partner,
        "method": method,
        "status": status,
        "latency_ms": latency,
        "error_code": error_code,
        "retry_attempted": retry_attempted,
        "recovered_after_retry": recovered_after_retry,
        "timestamp": time.time()
    }

    with open("data/logs.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")

async def main():

    async with httpx.AsyncClient() as client:

        tasks = []

        for _ in range(500):

            method = random.choice(PAYMENT_METHODS)

            partner = random.choice(PARTNERS)

            tasks.append(
                simulate_payment(
                    client,
                    method,
                    partner
                )
            )

        await asyncio.gather(*tasks)

asyncio.run(main())
