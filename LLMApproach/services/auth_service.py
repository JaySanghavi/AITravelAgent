import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")


def generate_token():

    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("Missing Amadeus credentials in .env")

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.text}")

    token_data = response.json()

    return token_data["access_token"]
