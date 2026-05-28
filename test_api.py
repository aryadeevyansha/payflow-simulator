import requests
import os
from dotenv import load_dotenv

load_dotenv()

KEY_ID = os.getenv("RAZORPAY_KEY_ID")
KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

url = "https://api.razorpay.com/v1/orders"

payload = {
    "amount": 50000,
    "currency": "INR",
    "receipt": "receipt_001"
}

response = requests.post(
    url,
    auth=(KEY_ID, KEY_SECRET),
    json=payload
)

print("STATUS CODE:", response.status_code)
print("RESPONSE:")
print(response.json())