import requests
import random
import time

TOKEN = "zv1EsR2CKcD5EyShCkuy"

URL = f"http://localhost:8085/api/v1/{TOKEN}/telemetry"

while True:

    data = {
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(60, 95), 2),
        "leaf_wetness": round(random.uniform(1, 10), 2),
        "rainfall": round(random.uniform(0, 10), 2)
    }

    response = requests.post(URL, json=data)

    print("Sent:", data)
    print("Status:", response.status_code)

    time.sleep(5)