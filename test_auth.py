#!/usr/bin/env python3
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test register
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
user_data = {
    "email": f"test{timestamp}@example.com",
    "username": f"testuser{timestamp}",
    "password": "pass123"
}

print("Testing registration...")
print(f"Payload: {json.dumps(user_data, indent=2)}")

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# If registration successful, test login
if response.status_code == 200:
    print("\nTesting login...")
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
