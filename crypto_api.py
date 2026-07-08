import requests
from config import COINGECKO_API_URL

def get_crypto_price(coin_id="bitcoin", currency="usd"):
    """Fetch current price for a cryptocurrency from CoinGecko"""
    try:
        url = f"{COINGECKO_API_URL}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": currency
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if coin_id in data and currency in data[coin_id]:
            return data[coin_id][currency]
        return None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def get_trending_coins():
    """Get top 7 trending cryptocurrencies"""
    try:
        url = f"{COINGECKO_API_URL}/search/trending"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        trending = []
        for item in data.get("coins", [])[:7]:
            coin = item.get("item", {})
            trending.append({
                "name": coin.get("name", "Unknown"),
                "symbol": coin.get("symbol", "").upper(),
                "price_btc": coin.get("price_btc", 0)
            })
        return trending
    except Exception as e:
        print(f"Error fetching trending: {e}")
        return []

def get_supported_coins():
    """Get list of supported coin IDs"""
    try:
        url = f"{COINGECKO_API_URL}/coins/list"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [coin["id"] for coin in data[:100]]  # First 100 for simplicity
    except Exception as e:
        print(f"Error fetching coin list: {e}")
        return []
