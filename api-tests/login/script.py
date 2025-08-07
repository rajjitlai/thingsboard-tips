import os
import requests
from dotenv import load_dotenv

load_dotenv()


def login_to_thingsboard():
    THINGSBOARD_URL = os.getenv("THINGSBOARD_URL")
    USERNAME = os.getenv("TB_USERNAME")
    PASSWORD = os.getenv("TB_PASSWORD")

    if not all([THINGSBOARD_URL, USERNAME, PASSWORD]):
        print("❌ Missing environment variables. Please check your .env file.")
        exit()

    login_url = f"{THINGSBOARD_URL}/api/auth/login"
    login_payload = {"username": USERNAME, "password": PASSWORD}
    login_response = requests.post(login_url, json=login_payload)

    if login_response.status_code != 200:
        print("❌ Login failed:", login_response.text)
        exit()

    token = login_response.json().get("token")
    return THINGSBOARD_URL, token
