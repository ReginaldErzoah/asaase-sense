import os

import httpx
from dotenv import load_dotenv

load_dotenv()

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

if not OPENAQ_API_KEY:
    raise ValueError("OPENAQ_API_KEY is missing. Check your .env file")