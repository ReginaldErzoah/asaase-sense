import os

import httpx
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAQ_API_KEY")

if api_key is None:
    raise ValueError("OPENAQ_API_KEY is missing. Check your .env file")

OPENAQ_API_KEY = api_key

BASE_URL = "https://api.openaq.org/v3"
TIMEOUT = 30.0


def get_client() -> httpx.Client:
    return httpx.Client(
        base_url=BASE_URL, headers={"X-API-Key": OPENAQ_API_KEY}, timeout=TIMEOUT
    )
