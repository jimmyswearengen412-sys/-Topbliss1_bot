import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# CoinGecko API (free, no API key needed)
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
