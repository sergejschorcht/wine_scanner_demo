import base64
import requests
import time

API_URL = "http://localhost:5328"

if __name__ == "__main__":
    start_time = time.time()

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"{API_URL}/api/retrieve",
        headers=headers
    )

    end_time = time.time()

    print(f"Base64-Request-Zeit: {(end_time - start_time):.2f} Sekunden")
    print("Response:", response.json())